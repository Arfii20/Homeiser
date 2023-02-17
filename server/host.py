"""Entry point for server"""

import click
from flask import Flask, g
from flask_restful import Api  # type: ignore
import mysql.connector


# Errors


class DBPasswordError(Exception):
    """No password supplied to the database"""


@click.group
def server():
    ...


app = Flask(__name__)
api = Api(app)


@app.teardown_appcontext
def close_connection(exception):
    """Closes db if sudden error"""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def get_db(passwd=None):
    """Returns current database connection"""
    db = getattr(g, "_database", None)
    if db is None:
        if passwd is None:
            raise DBPasswordError(
                "DB has not been initialised yet so password is needed"
            )
        db = g._database = mysql.connector.connect(
            host="localhost", user="root", password=input("DB Password: ")
        )
        # buffered = true may be needed
    return db


@click.option("-h", "--host", default="127.0.0.1")
@click.option("-d", "--debug", is_flag=True, default=True)
@click.option("--password", prompt="Database Password", hide_input=True)
@server.command()
def start(host: str, debug: bool, password: str):
    app.run(host=host, debug=debug)
    get_db(password)
