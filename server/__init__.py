from flask import Flask

def make_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "idkwhatimdoing"

    # from .shared_list import shared_list
    # from .shared_calender import shared_calendar

    return app