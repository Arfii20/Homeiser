import mysql.connector
from flask import g

"""Database handler is in its own file to avoid circular imports"""


class DBPasswordError(Exception):
    """No password supplied to the database"""


def get_db():
    """Returns current database connection if there is one. If not, creates one and asks for password via cli"""
    db = getattr(g, "_database", None)
    if db is None:
        while True:
            try:
                db = g._database = mysql.connector.connect(
                    host="localhost", user="root", password=input("DB Password: ")
                )
                break
            except mysql.connector.errors.ProgrammingError:
                print("Authentication failed")

        # buffered = true may be needed
    return db


