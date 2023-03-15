"""
The shared calendar methods are defined here
"""

from flask_restful import Resource, reqparse, abort
from server.db_handler import get_conn, get_db
from server.shared_list.Calendar_and_List_Builds import CalendarEventBuild
from json import dumps
import re

class GetSharedCalendar(Resource):
    def post(self, household_id):
        """
        Sends the event details in a specific time range to the website

        How get requests for calendar events should be:
        requests.post(BASE + "get_shared_calendar/<int: household_id>", {"starting_time": "yyyy-mm-dd HH:MM:SS",
                                                                    "ending_time": "yyyy-mm-dd HH:MM:SS"})

        :returns
        The server will return following json object:
        {
        [{event1}, {event2}, {event3}]
        }

        Each event has the following structure
        {
        'event_id': 3,
        'title_of_event': 'event_a',
        'starting_time': '2023-2-19 0:0:0'
        'ending_time': '2023-2-19 20:0:0',
        'additional_notes': 'Do this',
        'location_of_event': 'This address',
        'household_id': 1,
        'tagged_users': [1, 2, 4],
        'added_by': 7
        }

        *** For the times, have to use split() method of JS as it return 1 digit if the first digit is 0
        e.g. '2023-2-19 0:0:0' instead of '2023-02-19 00:00:00'

        if nothing in the time range, the lists will be empty
        """
        cursor = get_db()

        parser = reqparse.RequestParser()
        parser.add_argument(
            "starting_time",
            type=str,
            required=True,
            location="form",
            help="Starting time is required",
        )
        parser.add_argument(
            "ending_time",
            type=str,
            required=True,
            location="form",
            help="End time is required",
        )
        args = parser.parse_args()

        starting_time = args.get("starting_time")
        ending_time = args.get("ending_time")

        query = "SELECT * FROM calendar_event WHERE household_id = %s AND start_time >= '%s' AND end_time <= '%s';"
        data = (household_id, starting_time, ending_time)
        cursor.execute(query % data)
        fetched_result = cursor.fetchall()

        all_events = []
        if fetched_result:
            query1 = "SELECT * FROM user_doing_calendar_event"
            cursor.execute(query1)
            result = cursor.fetchall()
            for x in fetched_result:
                tagged = []
                added_by = -1
                for i in result:
                    if i[1] == x[0]:
                        tagged.append(i[0])
                        if i[2] != added_by:
                            added_by = i[2]
                event_objects = CalendarEventBuild(x, tagged, added_by)
                all_events.append(event_objects.build_calendar_event())

            all_events = dumps(all_events)

            return all_events, 200
        else:
            abort(404, error="No event found")

class SharedCalendar(Resource):
    def post(self, household_id):
        """
        Creates an event in the database by adding a new row

        The request should be like:
        requests.post(BASE + "shared_calendar/1", {"title_of_event": "event_a",
                                                  "starting_time": "yyyy-mm-dd HH:MM:SS",
                                                  "ending_time": "yyyy-mm-dd HH:MM:SS",
                                                  "additional_notes": "Information of the event",
                                                  "location_of_event": "Address_a",
                                                  "tagged_users": "4 5 3",
                                                  "added_by": 7})

        *** All should be strings apart from "added_by"

        :returns:
        If successful,
        {'message': 'Event Added'}
        """
        connection, cursor = get_conn()
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, location="form")
        parser.add_argument(
            "title_of_event",
            type=str,
            required=True,
            location="form",
            help="Title of the event is required",
        )
        parser.add_argument(
            "starting_time",
            type=str,
            required=True,
            location="form",
            help="Starting time is required",
        )
        parser.add_argument(
            "ending_time",
            type=str,
            required=True,
            location="form",
            help="End time is required",
        )
        parser.add_argument(
            "additional_notes",
            type=str,
            required=True,
            location="form",
            help="Details is required",
        )
        parser.add_argument(
            "location_of_event",
            type=str,
            required=True,
            location="form",
            help="Location is required",
        )
        parser.add_argument(
            "tagged_users",
            type=str,
            required=True,
            location="form",
            help="tagged users are required",
        )
        parser.add_argument(
            "added_by",
            type=int,
            required=True,
            location="form",
            help="User ID is required",
        )

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
            query = "SELECT * FROM calendar_event WHERE id = %s;"
            cursor.execute(query % event_id)
            if cursor.fetchall():
                abort(409, message="Cannot use this ID. Already exists")
            else:
                query = """ 
                            INSERT INTO calendar_event (id, title, start_time, end_time, notes, location, household_id)
                            VALUES(%s, '%s', '%s', '%s', '%s', '%s', %s);
                    """
                data = (
                    event_id,
                    title_of_event,
                    starting_time,
                    ending_time,
                    additional_notes,
                    location_of_event,
                    household_id,
                )
                cursor.execute(query % data)
                connection.commit()

                # For adding to the other table
                tagged_user_ids = tagged_user_ids.split()
                query_doing = """
                                INSERT INTO user_doing_calendar_event (user_id, calendar_event_id, added_by_user)
                                VALUES (%s, %s, %s)
                              """
                for i in tagged_user_ids:
                    data = (int(i), event_id, added_by)
                    cursor.execute(query_doing % data)
                    connection.commit()

                return {"message": "Event Added"}, 201
        else:
            query = """ 
                        INSERT INTO calendar_event (title, start_time, end_time, notes, location, household_id)
                        VALUES('%s', '%s', '%s', '%s', '%s', %s);
                """
            data = (
                title_of_event,
                starting_time,
                ending_time,
                additional_notes,
                location_of_event,
                household_id,
            )
            cursor.execute(query % data)
            connection.commit()

            query_for_id = """SELECT id FROM calendar_event ORDER BY id DESC LIMIT 1"""
            cursor.execute(query_for_id)
            events_id = cursor.fetchone()[0]
            connection.commit()

            tagged_user_ids = tagged_user_ids.split()
            query_doing = """
                            INSERT INTO user_doing_calendar_event (user_id, calendar_event_id, added_by_user)
                            VALUES (%s, %s, %s)
                          """
            for i in tagged_user_ids:
                data = (int(i), events_id, added_by)
                cursor.execute(query_doing % data)
                connection.commit()
            return {"message": "Event Added"}, 201


class CalendarEvent(Resource):
    def get(self, calendar_event_id):
        """
        Sends one event details when clicked on an event using the calendar_event_id

        How get requests for calendar events should be like:
        requests.get(BASE + "shared_calendar/<int: calendar_event_id>")

        :returns
        The server will return following json object:
        {
        'event_id': 3,
        'title_of_event': 'event_a',
        'starting_time': '2023-2-19 0:0:0'
        'ending_time': '2023-2-19 20:0:0',
        'additional_notes': 'Do this',
        'location_of_event': 'This address',
        'household_id': 1,
        'tagged_users': [1, 2, 4],
        'added_by': 7
        }

        *** For the times, have to use split() method of JS as it return 1 digit if the first digit is 0
        e.g. '2023-2-19 0:0:0' instead of '2023-02-19 00:00:00'

        if the list does not exist, it will show an error message
        """
        cursor = get_db()
        query = "SELECT * FROM calendar_event WHERE id = %s;"
        cursor.execute(query % calendar_event_id)

        fetched_result = cursor.fetchall()
        if fetched_result:
            query1 = (
                "SELECT * FROM user_doing_calendar_event WHERE calendar_event_id = %s"
            )
            cursor.execute(query1 % calendar_event_id)
            tagged = []
            added_by = -1
            for i in cursor.fetchall():
                tagged.append(i[0])
                if i[2] != added_by:
                    added_by = i[2]
            print(fetched_result)
            event_objects = CalendarEventBuild(fetched_result[0], tagged, added_by)
            objects = event_objects.build_calendar_event()

            return objects, 200
        else:
            abort(404, error="Event id does not exist")

    def put(self, calendar_event_id):
        """
        Inserts the event details into the database using the calendar_event_id

        How put requests for calendar events should be like:
        requests.put(BASE + "shared_calendar/<int: calendar_event_id>", {"title_of_event": "Party",
                                                                        "starting_time": "yyyy-mm-dd HH:MM:SS",
                                                                        "ending_time": "yyyy-mm-dd HH:MM:SS",
                                                                        "additional_notes": "Info of the event",
                                                                        "location_of_event": "This address",
                                                                        "tagged_users": "3 7",
                                                                        "added_by": 5
                                                                        })
        *** Everything should be string apart from 'added_by' which is int

        :returns:
        if successful,
        {"message": "Task details updated"}

        Error otherwise
        """
        connection, cursor = get_conn()
        parser = reqparse.RequestParser()
        parser.add_argument(
            "title_of_event",
            type=str,
            required=True,
            location="form",
            help="Title of the event is required",
        )
        parser.add_argument(
            "starting_time",
            type=str,
            required=True,
            location="form",
            help="Starting time is required",
        )
        parser.add_argument(
            "ending_time",
            type=str,
            required=True,
            location="form",
            help="End time is required",
        )
        parser.add_argument(
            "additional_notes",
            type=str,
            required=True,
            location="form",
            help="Details is required",
        )
        parser.add_argument(
            "location_of_event",
            type=str,
            required=True,
            location="form",
            help="Location is required",
        )
        parser.add_argument(
            "tagged_users",
            type=str,
            required=True,
            location="form",
            help="Tagged Users are required",
        )
        parser.add_argument(
            "added_by",
            type=int,
            required=True,
            location="form",
            help="Added by User is required",
        )
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

        query = "SELECT * FROM calendar_event WHERE id = %s;"
        cursor.execute(query % calendar_event_id)

        if cursor.fetchall():
            # Deleting from user doing calendar event
            query_delete = (
                "DELETE FROM user_doing_calendar_event WHERE calendar_event_id = %d"
            )
            cursor.execute(query_delete % calendar_event_id)
            connection.commit()

            # Add the new details to the same table
            tagged_user_ids = tagged_user_ids.split()
            query_doing = """
                            INSERT INTO user_doing_calendar_event (user_id, calendar_event_id, added_by_user)
                            VALUES (%s, %s, %s)
                          """
            for i in tagged_user_ids:
                data = (int(i), calendar_event_id, added_by)
                cursor.execute(query_doing % data)
                connection.commit()

            # Finally update the calendar event table
            query = (
                "UPDATE calendar_event "
                "SET title = '%s', "
                "    start_time = '%s', "
                "    end_time = '%s', "
                "    notes = '%s', "
                "    location = '%s'"
                "WHERE id = %s;"
            )
            data = (
                title_of_event,
                starting_time,
                ending_time,
                additional_notes,
                location_of_event,
                calendar_event_id,
            )
            cursor.execute(query % data)
            connection.commit()

            return {"message": "Task details updated"}, 200
        else:
            abort(406, message="Event does not exist")

    def delete(self, calendar_event_id):
        """
        How delete requests for calendar events should be like:
        message = requests.delete(BASE + "calendar_event/<int: calendar_event_id>")

        :returns:
        If successful,
        {'message': 'Calendar Event Deleted'}

        Otherwise, error.
        """
        connection, cursor = get_conn()
        cursor.execute(
            "SELECT * FROM calendar_event WHERE id = %s;" % calendar_event_id
        )
        present = cursor.fetchall()

        if present:
            query1 = (
                "DELETE FROM user_doing_calendar_event WHERE calendar_event_id = %d"
            )
            cursor.execute(query1 % calendar_event_id)
            connection.commit()

            query = "DELETE FROM calendar_event WHERE id = %s;"
            cursor.execute(query % calendar_event_id)
            connection.commit()
            return {"message": "Calendar Event Deleted"}, 200
        else:
            abort(404, message="Calendar Event Doesnt Exist")


class UserColour(Resource):
    def get(self, household_id):
        """
        Sends the colours assigned to individual users to the website




        How get requests for user_colours should be like:
        requests.get(BASE + "user_color/<int:household_id>")

        :returns:
        The server will return following json object:
        {
        'id': [3, 4],
        'color': [346523, 435465]
        }
        """
        cursor = get_db()
        query = "SELECT id, color FROM user WHERE household_id = %s;"
        cursor.execute(query % household_id)

        if cursor.fetchall():
            objects = {"id": [], "color": []}
            for x in cursor.fetchall():
                objects["id"].append(x[0])
                objects["color"].append(x[1])

            return objects, 200
        else:
            abort(404, error="Users or household id not found")
