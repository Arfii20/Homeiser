import mysql.connector
from flask import g


class DBPasswordError(Exception):
    """No password supplied to the database"""


def get_db():
    """Returns current database connection if there is one. If not, creates one and asks for password via cli"""
    db = getattr(g, "_database", None)

    # connect to db (ask for password). Ask for password again if wrong. Set mysql to use x5db
    if db is None:
        db = g._database = mysql.connector.connect(
            host="localhost", user="root", password="", buffered=True
        )

        db._execute_query("USE x5db;")

    return db
