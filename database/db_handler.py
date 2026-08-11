import mysql.connector as sql
from mysql.connector import errorcode
import os
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
            cursor = con.cursor()
            # print("Connection databse", self.database)
            query = f'USE {self.database}'
            cursor.execute(query)
            con.commit()
            print("Connected successfully!")
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
        con = self.connection()
        if not con:
            return False

        encrypted_pass = self.password_hash.userPassword(password)
        query = 'INSERT INTO ACCOUNT (name, username, email, password) VALUES (%s, %s, %s, %s)'
        try:
            cursor = con.cursor()
            cursor.execute(query, (name, username, email, encrypted_pass))
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
        self.login_successful = False
        con = self.connection()
        if not con:
            return False

        try:
            cursor = con.cursor()
            cursor.execute("SELECT password FROM ACCOUNT WHERE email = %s", (email,))
            data = cursor.fetchone()

            db_password_hash = data[0]

            if isinstance(db_password_hash, str):
                db_password_hash = db_password_hash.encode("utf-8")

            is_match = bcrypt.checkpw(password.encode('utf-8'), db_password_hash)
            if is_match:
                print("User exist!")
                print("Data:", data[0])
                self.login_successful = True
            else:
                print("Data:", data[0])
                print("User doesn't exist")
            # return db_password_hash

        except sql.Error as err:
            print("Error:", err)

        finally:
            cursor.close()
            con.close()

    # def getUser(self, email):
    #     con = self.connection()
    #     if not con:
    #         return False

    #     # query = 'SELECT password FROM ACCOUNT WHERE email = %s'
    #     try:
    #         cursor = con.cursor()
    #         cursor.execute("SELECT password FROM ACCOUNT WHERE email = %s", (email,))
    #         # con.commit()
    #         data = cursor.fetchall()
    #         self.db_password = data[0][0]
    #         # print(type(data))
    #         print(data[0][0])
    #         print("User found")

    #     except sql.Error as err:
    #         print("Error:", err)
