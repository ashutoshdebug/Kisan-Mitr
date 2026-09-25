import mysql.connector as sql
from mysql.connector import errorcode
import os
from pathlib import Path
import bcrypt
from utils.password_hash import PasswordHash
from dotenv import load_dotenv

load_dotenv()
# Connecting to the server

password_hash = PasswordHash()

class dbHandler:
    def __init__(self):
        self.host = os.getenv("db_host")
        # print("Host:", self.host)
        self.user = os.getenv("db_user")
        self.password = os.getenv("db_password")
        self.database = os.getenv("database")
        self.login_successful = False
        self.username = None
        self.imagePath = None
        self.resultPath = None
        self.user_already_exist = False
        self.user_not_exist = False
        self.profile_data = None
        # self.username_folder = None
        # print("Init database:", self.database)

    def connection(self):
        try:
            con = sql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            # cursor = con.cursor()
            # print("Connection databse", self.database)
            # query = f'USE {self.database}'
            # cursor.execute(query)
            # con.commit()
            # print("Connected successfully!")
            return con

        except sql.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("Error", err)

            return None

    def userRegistration(self, name, username, email, password):
        self.user_already_exist = False
        if not name or not username or not email or not password:
            # print("No sufficient data is provided to register user")
            return False

        con = self.connection()
        if not con:
            return False

        cursor = None

        lowerCaseEmail = str(email).lower()
        # print(lowerCaseEmail)
        encrypted_pass = self.password_hash.userPassword(password)
        query = "INSERT INTO ACCOUNT (name, username, email, password) VALUES (%s, %s, %s, %s)"
        try:
            cursor = con.cursor()
            cursor.execute(query, (name, username, lowerCaseEmail, encrypted_pass))
            con.commit()
            # print("Commited successfully")
            self.user_already_exist = False
            return True

        except sql.Error as err:
            # print("Error adding user:", err)
            self.user_already_exist = True
            return False

        finally:
            if cursor is not None:
                cursor.close()
            con.close()

    def verifyUser(self, password, email):
        self.login_successful = False
        self.username = None
        self.user_not_exist = False
        if not password or not email:
            print("No email and password are provided to verify the user")
            return False

        con = self.connection()

        if not con:
            return False

        cursor = None

        try:
            lowerCaseEmail = str(email).lower()
            # print(lowerCaseEmail)
            cursor = con.cursor()
            cursor.execute("SELECT username, password FROM ACCOUNT WHERE email = %s", (lowerCaseEmail,),)
            data = cursor.fetchone()

            if not data:
                # print("User doesn't exist")
                self.login_successful = False
                self.user_not_exist = True
                return False

            db_password_hash = data[1]

            if isinstance(db_password_hash, str):
                db_password_hash = db_password_hash.encode("utf-8")

            is_match = bcrypt.checkpw(password.encode("utf-8"), db_password_hash)
            if is_match:

                # self.username_folder = data[0]
                
                self.username = data[0]

                # self.createFolder(self.username_folder)
                # print("User exist!")
                # print("Data:", data[1])
                
                self.login_successful = True
                self.user_not_exist = False

                return True
            else:
                # print("Data:", data[1])
                # print("User doesn't exist")

                self.login_successful = False
                self.user_not_exist = True

                return False
            # return db_password_hash

        except sql.Error as err:
            print("Error:", err)

        finally:
            if cursor is not None:
                cursor.close()
            con.close()

    def addFolderPath(self, username, path):
        if not path or not username:
            print("No path or username found!")
            return False

        con = self.connection()
        if not con:
            return False

        cursor = None

        try:
            query = "INSERT INTO FILE_PATH (username, file_path) VALUES (%s, %s) ON DUPLICATE KEY UPDATE file_path = VALUES(file_path)"
            cursor = con.cursor()
            cursor.execute(query, (username, path,),)
            con.commit()
            # print("File path committed")
            return True

        except sql.Error as err:
            # print("File path database error:", err)
            return False

        finally:
            if cursor is not None:
                cursor.close()
            con.close()

    def addImageName(self, username, imageName):
        if not username or not imageName:
            return False

        con = self.connection()
        if not con:
            return False

        cursor = None

        try:
            query = "INSERT INTO IMAGE_NAME (username, image_name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE image_name = VALUES(image_name)"
            cursor = con.cursor()
            cursor.execute(query, (username, imageName))
            con.commit()
            # print("Image name committed")
            return True

        except sql.Error as err:
            print("Add image SQL error:", err)
            return False

        finally:
            if cursor is not None:
                cursor.close()
            con.close()

    def getImagePath(self, username):
        if not username:
            return False

        con = self.connection()
        if not con:
            return False

        cursor = None
        

        try:
            query = "SELECT file_path.file_path, image_name.image_name FROM file_path JOIN image_name ON file_path.username = image_name.username WHERE file_path.username = %s"
            cursor = con.cursor()
            cursor.execute(query, (username,))
            data = cursor.fetchone()

            # print("GetImagePath username:", username)
            # print("GetImagePath Database data:", data)

            if not data:
                print("No image record found for this user")
                return None

            self.imagePath = os.path.join(data[0], "image", data[1])

            # print("Image Path:", self.imagePath)
            return self.imagePath

        except sql.Error as err:
            # print("getImagePath SQL error:", err)
            return False

        finally:
            if cursor is not None:
                cursor.close()
            con.close()


    def insertCropProperties(self, username, location, crop_season, temperature, humidity, rainfall, windspeed, crop_variety, irrigation, soil, symptoms):
        if not username or not location or not crop_season or not crop_variety or not irrigation or not soil:
            return False

        if temperature is None or humidity is None or rainfall is None or windspeed is None:
            return False
        
        con = self.connection()
        if not con:
            return False

        cursor = None

        try:
            query = "INSERT INTO CROP_PROPERTIES (username, location, crop_season, temperature, humidity, rainfall, windspeed, crop_variety, irrigation, soil, symptoms) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE location = VALUES(location), crop_season = VALUES(crop_season), temperature = VALUES(temperature), humidity = VALUES(humidity), rainfall = VALUES(rainfall), windspeed = VALUES(windspeed), crop_variety = VALUES(crop_variety), irrigation = VALUES(irrigation), soil = VALUES(soil), symptoms = VALUES(symptoms)"
            cursor = con.cursor()
            cursor.execute(query, (username, location, crop_season, temperature, humidity, rainfall, windspeed, crop_variety, irrigation, soil, symptoms,))
            con.commit()
            # print("Insert Crop Properties committed")
            return True

        except sql.Error as err:
            # print("insertCropProperties error:", err)
            return False
        
        finally:
            if cursor is not None:
                cursor.close()
            con.close()

    def addResultName(self, username, result_file):
        if not username or not result_file:
            return False
        
        con = self.connection()
        if not con:
            return False
        
        cursor = None

        try:
            query = "INSERT INTO RESULT (username, result_file) VALUES (%s, %s) ON DUPLICATE KEY UPDATE result_file = VALUES(result_file)"
            cursor = con.cursor()
            cursor.execute(query, (username, result_file))
            con.commit()
            return True

        except sql.Error as err:
            # print("addResultName error:", err)
            return False

        finally:
            if cursor is not None:
                cursor.close()
            con.close()

    def getResultFilePath(self, username):
        if not username:
            return False
        
        con = self.connection()
        if not con:
            return False
        
        cursor = None

        try:
            query = "SELECT file_path.file_path, result.result_file FROM file_path JOIN result ON file_path.username = result.username WHERE file_path.username = %s"
            cursor = con.cursor()
            cursor.execute(query, (username,))
            data = cursor.fetchone()

            if not data:
                return False
            
            self.resultPath = os.path.join(data[0], "result", data[1])
            # print(data)
            return True

        except sql.Error as err:
            # print("getResultFilePath error:", err)
            return False

        finally:
            if cursor is not None:
                cursor.close()
            con.close()


    def getProfileData(self, username):
        self.profile_data = None

        con = self.connection()
        if not con:
            return False

        cursor = None
        # print("getProfileUsername:", username)
        try:
            query = "SELECT name, email, username FROM ACCOUNT WHERE username = %s"
            cursor = con.cursor()
            cursor.execute(query, (username,))
            data = cursor.fetchone()
            # print("GetProfileData:", data)

            self.profile_data = data

            # print("Profile name:", self.profile_name)
            # print("Profile email:", self.profile_email)
            # print("Profile username:", self.profile_username)

            return self.profile_data

        finally:
            pass