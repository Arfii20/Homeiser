import mysql.connector
from flask import g
from mysql.connector import cursor


class DBPasswordError(Exception):
    """No password supplied to the database"""


def get_conn() -> tuple[mysql.connector.MySQLConnection, cursor.MySQLCursor]:
    """Get a connection and a cursor to the database; overwrites connection in flask globals"""

    conn = g._database = mysql.connector.connect(
        host="localhost", user="root", password="HALR0b0t!12", database="x5db"
    )
    db = conn.cursor()

    return conn, db


def get_db() -> cursor.MySQLCursor:
    """Returns current database connection if there is one. If not, creates one and asks for password via cli"""
    db = getattr(g, "_database", None)

    # connect to db (ask for password). Ask for password again if wrong. Set mysql to use x5db
    if db is None:
        conn = g._database = mysql.connector.connect(
            host="localhost", user="root", password="HALR0b0t!12", database="x5db"
        )
        db = conn.cursor()

    return db
