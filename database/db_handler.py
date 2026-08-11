import mysql.connector as sql
from mysql.connector import errorcode
import os
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