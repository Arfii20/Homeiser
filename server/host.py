"""Entry point for server"""

import click
import flask_restful
from flask import Flask, g
from flask_restful import Api  # type: ignore

from server.db_handler import get_db
def create_app():
    """Ensures that database cursor can be accessed"""
    app = Flask(__name__)
    with app.app_context():
        get_db()

    return app

# create the app
app = create_app()
api = flask_restful.Api(app)

app.run()

import server.transaction_resources as tr


# Errors


@click.group
def server():
    ...

@app.teardown_appcontext
def close_connection(exception):
    """Closes db if sudden error"""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()



# add transaction resources
api.add_resource(tr.Transaction, "/")