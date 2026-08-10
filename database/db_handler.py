import mysql.connector as sql
from mysql.connector import errorcode
# Connecting to the server
try:
    con = sql.connect(
        host='',
        user='',
        password='',
    )
    print("Connected successfully!")

except sql.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Databasse does not exist")
    else:
        print("Error", err)

else: 
    con.close()