"""Entry point for server"""

from flask import Flask, g
from flask_cors import CORS
from flask_restful import Api  # type: ignore

import server.db_handler as db_handler
import server.endpoints as endpoints

# create the app
app = Flask(__name__)

CORS(app, resources={
    r"/get_shared_calendar/*": {"origins": "*"},
    r"/shared_calendar/*": {"origins": "*"},
    r"/calendar_event/*": {"origins": "*"},
    r"/user_attributes/*": {"origins": "*"},
    r"/shared_list/*": {"origins": "*"},
    r"/list_details/*": {"origins": "*"},
    r"/list_events/*": {"origins": "*"},
    r"/list_event_details/*": {"origins": "*"},
    r"/transaction/*": {"origins": "*"},
    r"/ledger/*": {"origins": "*"},
    r"/user/*": {"origins": "*"},
    r"/house/*": {"origins": "*"},
    r"/user_profile/*": {"origins": "*"},
    r"/group_details/*": {"origins": "*"},
    r"/simplify/*": {"origins": "*"},
    r"/transaction/as_events/*": {"origins": "*"},
    r"/login": {"origins": "*"}
})


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
