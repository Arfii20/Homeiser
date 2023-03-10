"""Entry point for server"""

from flask import Flask, g
from flask_restful import Api  # type: ignore

import server.db_handler as db_handler
import server.endpoints as endpoints
from flask_cors import CORS



# create the app
app = Flask(__name__)

cors = [
    CORS(app, resources={r"/shared_calender/*":{"origins": "*"}}),
    CORS(app, resources={r"/calender_event/*": {"origins": "*"}}),
    CORS(app, resources={r"/user_color/*": {"origins": "*"}}),
]

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
