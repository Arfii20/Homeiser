"""Entry point for server"""

from flask import Flask, g
from flask_restful import Api  # type: ignore

import server.db_handler as db_handler
import server.endpoints as endpoints

# create the app
app = Flask(__name__)
api = Api(app)
endpoints.attach(api)
app.run()

with app.app_context():
    conn = db_handler.get_db()


@app.teardown_appcontext
def close_connection(exception):
    """Closes db if sudden error"""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()
