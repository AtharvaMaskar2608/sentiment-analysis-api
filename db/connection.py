# db/connection.py

import mysql.connector
from mysql.connector import Error
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

from utils import setup_logger

# SETTING UP THE LOGGERR
logger = setup_logger()

def create_connection():
    """Create a database connection to the MySQL database."""
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            logger.info("Connected to database successfully!")
    except Error as e:
        logger.error(f"Error: '{e}' occurred while connecting to the database")
    return connection