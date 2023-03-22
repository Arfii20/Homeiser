"""Entry point for server"""

from flask import Flask, g
from flask_cors import CORS
from flask_restful import Api  # type: ignore

import server.db_handler as db_handler
import server.endpoints as endpoints

# create the app
app = Flask(__name__)

cors = [
        CORS(app, resources={r"/transaction/*": {"origins": "*"}}),
        CORS(app, resources={r"/ledger/*": {"origins": "*"}}),
        CORS(app, resources={r"/shared_list/*": {"origins": "*"}}),
        CORS(app, resources={r"/list_details/*": {"origins": "*"}}),
        CORS(app, resources={r"/list_events/*": {"origins": "*"}}),
        CORS(app, resources={r"/list_event_details/*": {"origins": "*"}}),
        CORS(app, resources={r"/get_shared_calendar/*": {"origins": "*"}}),
        CORS(app, resources={r"/shared_calendar/*": {"origins": "*"}}),
        CORS(app, resources={r"/calendar_event/*": {"origins": "*"}}),
        CORS(app, resources={r"/user_attributes/*": {"origins": "*"}}),
        CORS(app, resources={r"/user_profile/*": {"origins": "*"}}),
        CORS(app, resources={r"/group_details/*": {"origins": "*"}})
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
