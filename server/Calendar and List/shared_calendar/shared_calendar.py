"""
The shared calendar methods are defined here
"""

from flask import Flask
from flask_restful import Resource, Api, reqparse, abort
from mysql.connector import connect
import re

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


class SharedCalendar(Resource):

    def get(self, household_id):
        """
        Sends the event details to the website for display on calendar
        :return: returns part of the list
        """
        parser = reqparse.RequestParser()
        parser.add_argument("starting_time", type=str, required=True,
                            location="args", help="Starting time is required")
        parser.add_argument("ending_time", type=str, required=True,
                            location="args", help="End time is required")
        args = parser.parse_args()

        starting_time = args.get("starting_time")
        ending_time = args.get("ending_time")

        cursor = connection.cursor()
        query = "SELECT * FROM calendar_event WHERE household_id = %s AND start_time >= '%s' AND end_time <= '%s';"
        data = (household_id, starting_time, ending_time)
        cursor.execute(query % data)

        objects = {
            "id": [],
            "title_of_event": [],
            "starting_time": [],
            "ending_time": [],
            "household_id": [],
            "added_by": []
        }

        cursor1 = connection.cursor()
        query1 = "SELECT * FROM user_doing_calendar_event"
        cursor1.execute(query1)
        result = cursor1.fetchall()

        for x in cursor.fetchall():
            objects["id"].append(x[0])
            objects["title_of_event"].append(x[1])
            objects["starting_time"].append(
                f"{x[2].year}-{x[2].month}-{x[2].day} {x[2].hour}:{x[2].minute}:{x[2].second}")
            objects["ending_time"].append(
                f"{x[3].year}-{x[3].month}-{x[3].day} {x[3].hour}:{x[3].minute}:{x[3].second}")
            objects["household_id"].append(x[4])

            for i in result:
                if i[1] == x[0]:
                    objects["added_by"].append(i[2])
                    break

        return objects, 202

    def post(self, household_id):
        """
        Creates an event in the database
        :return: sends the event back for display
        """
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, location="form")
        parser.add_argument("title_of_event", type=str, required=True, location="form",
                            help="Title of the event is required")
        parser.add_argument("starting_time", type=str, required=True,
                            location="form", help="Starting time is required")
        parser.add_argument("ending_time", type=str, required=True,
                            location="form", help="End time is required")
        parser.add_argument("additional_notes", type=str, required=True,
                            location="form", help="Details is required")
        parser.add_argument("location_of_event", type=str, required=True,
                            location="form", help="Location is required")
        parser.add_argument("tagged_users", type=str, required=True,
                            location="form", help="tagged users are required")
        parser.add_argument("added_by", type=int, required=True,
                            location="form", help="User ID is required")

        args = parser.parse_args()
        event_id = args.get("id")
        title_of_event = args.get("title_of_event")
        starting_time = args.get("starting_time")
        ending_time = args.get("ending_time")
        additional_notes = args.get("additional_notes")
        location_of_event = args.get("location_of_event")
        tagged_user_ids = args.get("tagged_users")
        added_by = args.get("added_by")

        if event_id:
            cursor1 = connection.cursor()
            query = "SELECT * FROM calendar_event WHERE id = %s;"
            cursor1.execute(query % event_id)
            if cursor1.fetchone():
                abort(406, message="Cannot use this ID. Already exists")
            else:
                cursor = connection.cursor()
                query = """ 
                            INSERT INTO calendar_event (id, title, start_time, end_time, notes, location, household_id)
                            VALUES(%s, '%s', '%s', '%s', '%s', '%s', %s);
                    """
                data = (event_id, title_of_event, starting_time, ending_time,
                        additional_notes, location_of_event, household_id)
                cursor.execute(query % data)
                connection.commit()

                # For adding to the other table
                tagged_user_ids = tagged_user_ids.split()
                cursor2 = connection.cursor()
                query_doing = """
                                INSERT INTO user_doing_calendar_event (user_id, calendar_event_id, added_by_user)
                                VALUES (%s, %s, %s)
                              """
                for i in tagged_user_ids:
                    data = (int(i), event_id, added_by)
                    cursor2.execute(query_doing % data)
                    connection.commit()

                return {"Response": "Event Added"}, 201
        else:
            cursor = connection.cursor()
            query = """ 
                        INSERT INTO calendar_event (title, start_time, end_time, notes, location, household_id)
                        VALUES('%s', '%s', '%s', '%s', '%s', %s);
                """
            data = (title_of_event, starting_time, ending_time, additional_notes, location_of_event, household_id)
            cursor.execute(query % data)
            connection.commit()

            cursor1 = connection.cursor()
            query_for_id = "SELECT AUTO_INCREMENT FROM information_schema.tables " \
                           "WHERE table_name = 'calendar_event' AND table_schema = DATABASE( )"
            cursor1.execute(query_for_id)
            events_id = cursor1.fetchone()[0] - 1
            connection.commit()

            tagged_user_ids = tagged_user_ids.split()
            cursor2 = connection.cursor()
            query_doing = """
                            INSERT INTO user_doing_calendar_event (user_id, calendar_event_id, added_by_user)
                            VALUES (%s, %s, %s)
                          """
            for i in tagged_user_ids:
                data = (int(i), events_id, added_by)
                cursor2.execute(query_doing % data)
                connection.commit()
            return {"Response": "Event Added"}, 201


class CalendarEvent(Resource):

    def get(self, calendar_event_id):
        """
        Sending the event to the website when clicked on the event name from the calender
        :return: returns the whole event details
        """
        cursor = connection.cursor()
        query = "SELECT * FROM calendar_event WHERE id = %s;"
        cursor.execute(query % calendar_event_id)
        cursor1 = connection.cursor()
        query1 = "SELECT * FROM user_doing_calendar_event WHERE calendar_event_id = %s"
        cursor1.execute(query1 % calendar_event_id)
        for i in cursor1.fetchall():
            print(i)
        objects = {
            "event_id": [],
            "title_of_event": [],
            "starting_time": [],
            "ending_time": [],
            "additional_notes": [],
            "location_of_event": [],
            "household_id": [],
            "tagged_users": [],
            "added_by": []}
        for x in cursor.fetchall():
            objects["event_id"].append(x[0])
            objects["title_of_event"].append(x[1])
            objects["starting_time"].append(
                f"{x[2].year}-{x[2].month}-{x[2].day} {x[2].hour}:{x[2].minute}:{x[2].second}")
            objects["ending_time"].append(
                f"{x[3].year}-{x[3].month}-{x[3].day} {x[3].hour}:{x[3].minute}:{x[3].second}")
            objects["additional_notes"].append(x[4])
            objects["location_of_event"].append(x[5])
            objects["household_id"].append(x[6])

        cursor1 = connection.cursor()
        query1 = "SELECT * FROM user_doing_calendar_event WHERE calendar_event_id = %s"
        cursor1.execute(query1 % calendar_event_id)
        for i in cursor1.fetchall():
            if objects["event_id"][0] == i[1]:
                objects["tagged_users"].append(i[0])
                if i[2] not in objects["added_by"]:
                    objects["added_by"].append(i[2])

        return objects, 202

    def put(self, calendar_event_id):
        """
        Sends the event details to the database
        :return: the updated details
        """
        parser = reqparse.RequestParser()
        parser.add_argument("title_of_event", type=str, required=True, location="form",
                            help="Title of the event is required")
        parser.add_argument("starting_time", type=str, required=True,
                            location="form", help="Starting time is required")
        parser.add_argument("ending_time", type=str, required=True,
                            location="form", help="End time is required")
        parser.add_argument("additional_notes", type=str, required=True,
                            location="form", help="Details is required")
        parser.add_argument("location_of_event", type=str, required=True,
                            location="form", help="Location is required")
        parser.add_argument("tagged_users", type=str, required=True,
                            location="form", help="Tagged Users are required")
        parser.add_argument("added_by", type=int, required=True,
                            location="form", help="Added by User is required")
        args = parser.parse_args()
        title_of_event = args.get("title_of_event")
        starting_time = args.get("starting_time")
        ending_time = args.get("ending_time")
        additional_notes = args.get("additional_notes")
        location_of_event = args.get("location_of_event")
        tagged_user_ids = args.get("tagged_users")
        added_by = args.get("added_by")

        regex = "^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"
        if not re.search(regex, starting_time) or not re.search(regex, ending_time):
            abort(406, message="Format of date is wrong")

        cursor1 = connection.cursor()
        query = "SELECT * FROM calendar_event WHERE id = %s;"
        cursor1.execute(query % calendar_event_id)

        if cursor1.fetchone():
            # Deleting from user doing calendar event
            cursor2 = connection.cursor()
            query_delete = "DELETE FROM user_doing_calendar_event WHERE calendar_event_id = %d"
            cursor2.execute(query_delete % calendar_event_id)
            connection.commit()

            # Add the new details to the same table
            tagged_user_ids = tagged_user_ids.split()
            cursor3 = connection.cursor()
            query_doing = """
                            INSERT INTO user_doing_calendar_event (user_id, calendar_event_id, added_by_user)
                            VALUES (%s, %s, %s)
                          """
            for i in tagged_user_ids:
                data = (int(i), calendar_event_id, added_by)
                cursor3.execute(query_doing % data)
                connection.commit()

            # Finally update the calendar event table
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

            return {"Response": "Task details updated"}, 201
        else:
            abort(406, message="Event does not exist")

    def delete(self, calendar_event_id):
        """
        Delete event from the database (Either by the user who created or after end time)
        :return: None
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM calendar_event WHERE id = %s;" % calendar_event_id)
        present = cursor.fetchone()

        if present:
            cursor2 = connection.cursor()
            query1 = "DELETE FROM user_doing_calendar_event WHERE calendar_event_id = %d"
            cursor2.execute(query1 % calendar_event_id)
            connection.commit()

            query = "DELETE FROM calendar_event WHERE id = %s;"
            cursor1 = connection.cursor()
            cursor1.execute(query % calendar_event_id)
            connection.commit()
            return {'Response': 'Calendar Event Deleted'}, 202
        else:
            abort(404, message='Calendar Event Doesnt Exist')


class UserColour(Resource):
    def get(self):
        """
        Adds the birthdays of the users to the calendar
        :return: color of the user
        """
        cursor = connection.cursor()
        query = "SELECT id, color FROM user;"
        cursor.execute(query)

        objects = {
            "id": [],
            "color": []
        }
        for x in cursor.fetchall():
            objects["id"].append(x[0])
            objects["color"].append(x[1])

        return objects, 202


api.add_resource(SharedCalendar, "/shared_calendar/<int:household_id>")
api.add_resource(CalendarEvent, "/calendar_event/<int:calendar_event_id>")
api.add_resource(UserColour, "/user_color/")

if __name__ == '__main__':
    app.run(debug=True)
