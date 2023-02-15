"""
The shared calendar methods are defined here
"""

from flask import Blueprint, Flask, request
from flask_restful import Resource, Api
from mysql.connector import connect, Error


app = Flask(__name__)
api = Api(app)

shared_calendar = Blueprint("shared_calendar", __name__)


connection = connect(
                        host="localhost",
                        user="root",
                        password="Arfi12000@",
                    )

# api = Api(app)
print(connection)


class SharedCalender(Resource):

    def __init__(self):
        pass

    @app.route("/calender_events", methods=["GET", "POST"])
    def create_event(self):
        """
        Creates an event in the database
        :return: sends the event back for display
        """
        # INSERT INTO calender_event (title, start_time, end_time, notes, location, household_id)
        # VALUES(title_of_event, starting_time, ending_time, additional_notes, location_of_event, house_id);

        # SELECT * FROM calender_event;

    @app.route("/calender_events")
    def send_calender_event(self):
        """
        Sends the event details to the website for display on calender
        :return: returns part of the list
        """
        # SELECT title, start_time, end_time, house_id FROM calender_event;

    @app.route("/calender_events")
    def when_clicked_send_calendar_event(self):
        """
        Sending the event to the website when clicked on the event name from the calender
        :return: returns the whole event details
        """

        # SELECT * FROM calender_event;

    @app.route("/calender_events")
    def update_calendar_event(self):
        """
        Sends the event details to the database
        :return: the updated details
        """
        # SET title = new_task,
        #     start_time = new_start_time,
        #     end_time = new_end_time,
        #     notes = new_notes,
        #     location = new_location; # we can use the old value if the value not changed

    @app.route("/calender_events")
    def delete_calendar_event(self):
        """
        Delete event from the database (Either by the user who created or after end time)
        :return: None
        """

        # DELETE FROM calender_event WHERE id = Something;

    @app.route("/calender_events")
    def birthday_calendar_event(self):
        """
        Adds the birthdays of the users to the calendar
        :return: birthday of the user
        """
        # SELECT date_of_birth FROM user;
        # # Start time - 00:00 and end time - 23:59

    @app.route("/calender_events")
    def tag_in_calendar_event(self):
        """
        gets the id of the user for tagging
        :return: All the tagged ids
        """
        # SELECT id FROM user;
        # # Then tag all the ids maybe?

    @app.route("/calender_events")
    def user_color(self):
        """
        Selects a colour for
        :return:
        """
        # SELECT colour FROM user;


api.add_resource(SharedCalender, "/shared_list/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
