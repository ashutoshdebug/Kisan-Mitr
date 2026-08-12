import mysql.connector as sql
from mysql.connector import errorcode
import os
from pathlib import Path
import bcrypt
from utils.password_hash import PasswordHash
from dotenv import load_dotenv
load_dotenv()
# Connecting to the server

class dbHandler:
    def __init__(self):
        self.host = os.getenv("host")
        # print("Host:", self.host)
        self.user = os.getenv("user")
        self.password = os.getenv("password")
        self.database = os.getenv("database")
        self.login_successful = False
        # print("Init database:", self.database)
        self.password_hash = PasswordHash()

    def connection(self):
        try:
            con = sql.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database,
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
        if not (name and username and email and password):
            print("No sufficient data is provided to register user")
            return False

        con = self.connection()
        if not con:
            return False

        lowerCaseEmail = str(email).lower()
        # print(lowerCaseEmail)
        encrypted_pass = self.password_hash.userPassword(password)
        query = 'INSERT INTO ACCOUNT (name, username, email, password) VALUES (%s, %s, %s, %s)'
        try:
            cursor = con.cursor()
            cursor.execute(query, (name, username, lowerCaseEmail, encrypted_pass))
            con.commit()
            print("Commited successfully")
            return True

        except sql.Error as err:
            print("Error adding user:", err)
            return False

        finally:
            cursor.close()
            con.close()

    def verifyUser(self, password, email):
        if not (password and email):
            print("No email and password are provided to verify the user")
            return False
        
        con = self.connection()
        if not con:
            return False

        try:
            lowerCaseEmail = str(email).lower()
            print(lowerCaseEmail)
            cursor = con.cursor()
            cursor.execute("SELECT username, password FROM ACCOUNT WHERE email = %s", (lowerCaseEmail,))
            data = cursor.fetchone()

            if not data:
                print("User doesn't exist")
                self.login_successful = False
                return False

            db_password_hash = data[1]

            if isinstance(db_password_hash, str):
                db_password_hash = db_password_hash.encode("utf-8")

            is_match = bcrypt.checkpw(password.encode('utf-8'), db_password_hash)
            if is_match:
                self.username_folder = data[0]
                self.createFolder(self.username_folder)
                print("User exist!")
                print("Data:", data[1])
                self.login_successful = True
            else:
                print("Data:", data[1])
                print("User doesn't exist")
            # return db_password_hash

        except sql.Error as err:
            print("Error:", err)

        finally:
            cursor.close()
            con.close()
            

    def createFolder(self, username):
        self.folder_path = None
        # exist = False
        if not username:
            print("Folder creation failed: No username supplied")
            return False
        
        folder_name = username
        self.sanitize_name = os.path.basename(folder_name)
        BASE_DIR = Path(__file__).resolve().parent.parent
        # print("Base dir:", BASE_DIR)
        path = BASE_DIR/ "static" / "uploads" / "database" / self.sanitize_name

        try:
            print("Create folder username:", self.sanitize_name)

            if path.exists():
                self.addFolderPath(self.sanitize_name, str(path))
                return True
                # exist = True
                # print("Folder exist:", exist)

            else:
                path.mkdir(parents=True, exist_ok=True)
                # print(str(path))
                self.addFolderPath(self.sanitize_name, str(path))
                return True
                # exist = False
                # print("Folder doesn't exist:", exist)
        
        except OSError as err:
            print("Create folder filesystem error:", err)

        except Exception as err:
            print("Unexpected error:", err)

    def addFolderPath(self, username, path):
        if not path and username:
            print("No path or username found!")
            return False

        con = self.connection()
        if not con:
            return False

        try:
            query = "INSERT INTO FILE_PATH (username, file_path) VALUES (%s, %s)"
            cursor = con.cursor()
            cursor.execute(query, (username, path,))
            con.commit()
            print("File path commited")

        except sql.Error as err:
            print("File path database error:", err)

        finally:
            cursor.close()
            con.close()