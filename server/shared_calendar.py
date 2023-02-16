"""
The shared calendar methods are defined here
"""

from flask import Flask
from flask_restful import Resource, Api, reqparse
from mysql.connector import connect, Error
import datetime

app = Flask(__name__)
api = Api(app)

# def get_db():
connection = connect(
    host="localhost",
    user="root",
    password="Arfi12000@",
    database="x5db",
    buffered=True
)
print(connection)


class SharedCalendar(Resource):

    def post(self, household_id):
        """
        Creates an event in the database
        :return: sends the event back for display
        """
        parser = reqparse.RequestParser()
        parser.add_argument("title_of_event", type=str, required=True, location="form",
                            help="Title of the event is required")
        parser.add_argument("starting_time", type=list, required=True,
                            location="form", help="Starting time is required")
        parser.add_argument("ending_time", type=list, required=True,
                            location="form", help="End time is required")
        parser.add_argument("additional_notes", type=str, required=True,
                            location="form", help="Details is required")
        parser.add_argument("location_of_event", type=str, required=True,
                            location="form", help="Location is required")
        args = parser.parse_args()
        title_of_event = args.get("title_of_event")
        st = args.get("starting_time")
        et = args.get("ending_time")
        additional_notes = args.get("additional_notes")
        location_of_event = args.get("location_of_event")

        cursor = connection.cursor()
        query = """ 
                    INSERT INTO calender_event (title, start_time, end_time, notes, location, household_id)
                    VALUES('%s', '%s', '%s', '%s', '%s', %s);
                """
        data = (title_of_event, datetime.datetime(st[0], st[1], st[2], st[3], st[4], st[5]),
                datetime.datetime(et[0], et[1], et[2], et[3], et[4], et[5]),
                additional_notes, location_of_event, household_id)
        cursor.execute(query % data)
        connection.commit()
        print("Hello")
        return {"Response": "EventAdded"}, 271

    def get(self, household_id):
        """
        Sends the event details to the website for display on calender
        :return: returns part of the list
        """
        cursor = connection.cursor()
        query = "SELECT title, start_time, end_time FROM calendar_event WHERE household_id = %s;"
        cursor.execute(query % household_id)

        objects = []
        for x in cursor.fetchall():
            objects.append(x)
            print(x)

        return {"Response": "Works"}, 272  # <-------------------------------------------------------


class CalendarEvent(Resource):

    def get(self, calendar_event_id):
        """
        Sending the event to the website when clicked on the event name from the calender
        :return: returns the whole event details
        """
        cursor = connection.cursor()
        query = "SELECT * FROM calendar_event WHERE id = %s;"
        cursor.execute(query % calendar_event_id)

        objects = []
        for x in cursor.fetchall():
            objects.append(x)
            print(x)

        return {"Response": "Works"}, 273

    def put(self, calendar_event_id):
        """
        Sends the event details to the database
        :return: the updated details
        """
        parser = reqparse.RequestParser()
        parser.add_argument("title_of_event", type=str, required=True, location="form",
                            help="Title of the event is required")
        parser.add_argument("starting_time", type=list, required=True,
                            location="form", help="Starting time is required")
        parser.add_argument("ending_time", type=list, required=True,
                            location="form", help="End time is required")
        parser.add_argument("additional_notes", type=str, required=True,
                            location="form", help="Details is required")
        parser.add_argument("location_of_event", type=str, required=True,
                            location="form", help="Location is required")
        args = parser.parse_args()
        title_of_event = args.get("title_of_event")
        starting_time = args.get("starting_time")
        ending_time = args.get("ending_time")
        additional_notes = args.get("additional_notes")
        location_of_event = args.get("location_of_event")

        cursor = connection.cursor()

        query = "UPDATE calendar_event " \
                "SET title = '%s', " \
                "    start_time = '%s', " \
                "    end_time = '%s', " \
                "    notes = '%s', " \
                "    location = '%s'" \
                "WHERE id = %s;"
        data = (title_of_event, starting_time, ending_time, additional_notes, location_of_event, calendar_event_id)
        cursor.execute(query % data)
        connection.commit()

        return {"Response": "Task details updated"}, 274

    def delete(self, calendar_event_id):
        """
        Delete event from the database (Either by the user who created or after end time)
        :return: None
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM calendar_event WHERE id = %s;" % calendar_event_id)
        present = cursor.fetchone()

        if present is not None:
            query = "DELETE FROM calendar_event WHERE id = %s;"
            cursor1 = connection.cursor()
            cursor1.execute(query % calendar_event_id)
            connection.commit()
            return {'Response': 'CalendarEventDeleted'}, 275
        else:
            return {'Response': 'CalendarEventDoesntExist'}, 276

class UserAttributes(Resource):
    def get(self):
        """
        Adds the birthdays of the users to the calendar
        :return: birthday of the user
        """
        cursor = connection.cursor()
        query = "SELECT id, date_of_birth, color FROM user;"
        cursor.execute(query)

        objects = []
        for x in cursor.fetchall():
            objects.append(x)
            print(x)

        return {"Response": "Works"}, 277
        #

    def tag_in_calendar_event(self):
        """
        gets the id of the user for tagging
        :return: All the tagged ids
        """
        # SELECT id FROM user;
        # # Then tag all the ids maybe?


api.add_resource(SharedCalendar, "/shared_calendar/<int:household_id>")
api.add_resource(CalendarEvent, "/calendar_event/<int:calendar_event_id>")
api.add_resource(UserAttributes, "/user_attributes/")

if __name__ == '__main__':
    app.run(debug=True)
