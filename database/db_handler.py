import os

import bcrypt
import mysql.connector as sql
from dotenv import load_dotenv
from mysql.connector import errorcode

from utils.password_hash import PasswordHash


load_dotenv()

DEFAULT_PROFILE_IMAGE = "uploads/frontend/default-profile.svg"


class dbHandler:
    def __init__(self):
        self.host = os.getenv("db_host")
        self.user = os.getenv("db_user")
        self.password = os.getenv("db_password")
        self.database = os.getenv("database")

        self.login_successful = False
        self.username = None
        self.imagePath = None
        self.resultPath = None

        self.user_already_exist = False
        self.user_not_exist = False

        self.password_hash = PasswordHash()

    def connection(self):
        try:
            return sql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

        except sql.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("Error", err)

            return None

    def userRegistration(
        self,
        name,
        username,
        email,
        password
    ):
        self.user_already_exist = False

        if not name or not username or not email or not password:
            return False

        con = self.connection()

        if not con:
            return False

        cursor = None

        try:
            encrypted_pass = self.password_hash.userPassword(password)

            query = """
                INSERT INTO ACCOUNT
                (name, username, email, password)
                VALUES (%s, %s, %s, %s)
            """

            cursor = con.cursor()
            cursor.execute(
                query,
                (
                    name,
                    username,
                    str(email).lower(),
                    encrypted_pass
                )
            )

            con.commit()
            return True

        except sql.Error as err:
            print("Registration SQL error:", err)
            self.user_already_exist = True
            return False

        finally:
            if cursor:
                cursor.close()

            con.close()

    def createUserProfile(self, username):
        if not username:
            return False

        con = self.connection()

        if not con:
            return False

        cursor = None

        try:
            query = """
                INSERT INTO user_profile
                (username, profile_image)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                profile_image = COALESCE(
                    profile_image,
                    VALUES(profile_image)
                )
            """

            cursor = con.cursor()
            cursor.execute(
                query,
                (
                    username,
                    DEFAULT_PROFILE_IMAGE
                )
            )

            con.commit()
            return True

        except sql.Error as err:
            print("Create profile SQL error:", err)
            return False

        finally:
            if cursor:
                cursor.close()

            con.close()

    def getUserProfile(self, username):
        if not username:
            return None

        con = self.connection()

        if not con:
            return None

        cursor = None

        try:
            query = """
                SELECT
                    account.name,
                    account.email,
                    user_profile.profile_image
                FROM account
                LEFT JOIN user_profile
                    ON account.username = user_profile.username
                WHERE account.username = %s
            """

            cursor = con.cursor(dictionary=True)
            cursor.execute(query, (username,))

            return cursor.fetchone()

        except sql.Error as err:
            print("Get profile SQL error:", err)
            return None

        finally:
            if cursor:
                cursor.close()

            con.close()

    def saveProfileImage(self, username, image_path):
        if not username or not image_path:
            return False

        con = self.connection()

        if not con:
            return False

        cursor = None

        try:
            query = """
                INSERT INTO user_profile
                (username, profile_image)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                profile_image = VALUES(profile_image)
            """

            cursor = con.cursor()
            cursor.execute(
                query,
                (username, image_path)
            )

            con.commit()
            return True

        except sql.Error as err:
            print("Save profile image SQL error:", err)
            return False

        finally:
            if cursor:
                cursor.close()

            con.close()

    def verifyUser(self, password, email):
        self.login_successful = False
        self.username = None
        self.user_not_exist = False

        if not password or not email:
            print("No email and password are provided")
            return False

        con = self.connection()

        if not con:
            return False

        cursor = None

        try:
            cursor = con.cursor()

            cursor.execute(
                """
                SELECT username, password
                FROM ACCOUNT
                WHERE email = %s
                """,
                (str(email).lower(),)
            )

            data = cursor.fetchone()

            if not data:
                self.user_not_exist = True
                return False

            db_password_hash = data[1]

            if isinstance(db_password_hash, str):
                db_password_hash = db_password_hash.encode("utf-8")

            if bcrypt.checkpw(
                password.encode("utf-8"),
                db_password_hash
            ):
                self.username = data[0]
                self.login_successful = True
                return True

            self.user_not_exist = True
            return False

        except sql.Error as err:
            print("Error:", err)
            return False

        finally:
            if cursor:
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
            query = """
                INSERT INTO FILE_PATH
                (username, file_path)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                file_path = VALUES(file_path)
            """

            cursor = con.cursor()
            cursor.execute(query, (username, path))

            con.commit()
            return True

        except sql.Error:
            return False

        finally:
            if cursor:
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
            query = """
                INSERT INTO IMAGE_NAME
                (username, image_name)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                image_name = VALUES(image_name)
            """

            cursor = con.cursor()
            cursor.execute(
                query,
                (username, imageName)
            )

            con.commit()
            return True

        except sql.Error as err:
            print("Add image SQL error:", err)
            return False

        finally:
            if cursor:
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
            query = """
                SELECT
                    file_path.file_path,
                    image_name.image_name
                FROM file_path
                JOIN image_name
                    ON file_path.username = image_name.username
                WHERE file_path.username = %s
            """

            cursor = con.cursor()
            cursor.execute(query, (username,))

            data = cursor.fetchone()

            if not data:
                print("No image record found for this user")
                return None

            self.imagePath = os.path.join(
                data[0],
                "image",
                data[1]
            )

            return self.imagePath

        except sql.Error as err:
            print("getImagePath SQL error:", err)
            return False

        finally:
            if cursor:
                cursor.close()

            con.close()

    def insertCropProperties(
        self,
        username,
        location,
        crop_season,
        temperature,
        humidity,
        rainfall,
        windspeed,
        crop_variety,
        irrigation,
        soil,
        symptoms
    ):
        if (
            not username
            or not location
            or not crop_season
            or not crop_variety
            or not irrigation
            or not soil
        ):
            return False

        if (
            temperature is None
            or humidity is None
            or rainfall is None
            or windspeed is None
        ):
            return False

        con = self.connection()

        if not con:
            return False

        cursor = None

        try:
            query = """
                INSERT INTO CROP_PROPERTIES
                (
                    username,
                    location,
                    crop_season,
                    temperature,
                    humidity,
                    rainfall,
                    windspeed,
                    crop_variety,
                    irrigation,
                    soil,
                    symptoms
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s
                )
                ON DUPLICATE KEY UPDATE
                    location = VALUES(location),
                    crop_season = VALUES(crop_season),
                    temperature = VALUES(temperature),
                    humidity = VALUES(humidity),
                    rainfall = VALUES(rainfall),
                    windspeed = VALUES(windspeed),
                    crop_variety = VALUES(crop_variety),
                    irrigation = VALUES(irrigation),
                    soil = VALUES(soil),
                    symptoms = VALUES(symptoms)
            """

            cursor = con.cursor()
            cursor.execute(
                query,
                (
                    username,
                    location,
                    crop_season,
                    temperature,
                    humidity,
                    rainfall,
                    windspeed,
                    crop_variety,
                    irrigation,
                    soil,
                    symptoms
                )
            )

            con.commit()
            return True

        except sql.Error:
            return False

        finally:
            if cursor:
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
            query = """
                INSERT INTO RESULT
                (username, result_file)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE
                result_file = VALUES(result_file)
            """

            cursor = con.cursor()
            cursor.execute(
                query,
                (username, result_file)
            )

            con.commit()
            return True

        except sql.Error:
            return False

        finally:
            if cursor:
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
            query = """
                SELECT
                    file_path.file_path,
                    result.result_file
                FROM file_path
                JOIN result
                    ON file_path.username = result.username
                WHERE file_path.username = %s
            """

            cursor = con.cursor()
            cursor.execute(query, (username,))

            data = cursor.fetchone()

            if not data:
                return False

            self.resultPath = os.path.join(
                data[0],
                "result",
                data[1]
            )

            return True

        except sql.Error:
            return False

        finally:
            if cursor:
                cursor.close()

            con.close()