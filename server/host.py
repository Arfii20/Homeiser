"""Entry point for server"""


import click
from flask import Flask, g
from flask_restful import Api  # type: ignore
import mysql.connector



@click.group
def server(): ...

app = Flask(__name__)
api = Api(app)

@app.teardown_appcontext
def close_connection(exception):
    """Closes db if sudden error"""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def get_db(passwd):
    """Returns current database connection"""
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = mysql.connector.connect(host="localhost", user="root", password=input("DB Password: "))
        # buffered = true may be needed
    return db

@click.option("-h", "--host", default="127.0.0.1")
@click.option("-d", "--debug", is_flag=True, default=True)
@click.option("--password", prompt="Database Password", hide_input=True)
@server.command()
def start(host: str, debug: bool, password: str ="HALR0b0t!12"):
    app.run(host=host, debug=debug)
    get_db(password)

