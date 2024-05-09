# models.py file
from mysql.connector import connect, Error
import os
from dotenv import load_dotenv
load_dotenv()

def connectToDB():
    try:
        connection = connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        return connection
    except Error as err:
        print("Error while connecting to the database:", err)
        return None