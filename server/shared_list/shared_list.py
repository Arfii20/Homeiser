"""
The shared list methods are defined here
"""

from json import dumps

from flask_restful import Resource, reqparse, abort

from server.db_handler import get_conn, get_db
from .Calendar_and_List_Builds import ListEventBuild, ListBuild


class SharedList(Resource):
    def get(self, household_id):
        """
        Sends the lists of a particular household using household_id

        How get requests for lists should be:
        requests.get(BASE + "shared_list/<int: household_id>")

        :returns
        The server will return following json object:
        {
        [{list1}, {list2}, {list3}],                                            # list of json objects
        }

        List has the following structure:
        {
        id': 1,
        'name': 'list1',
        'household_id': 1
        }

        if nothing is found, returns error message
        """
        cursor = get_db()

        cursor.execute("SELECT * FROM list WHERE household_id = %s;" % household_id)
        fetched_result = cursor.fetchall()

        if fetched_result:
            all_lists = []
            for x in fetched_result:
                list_build = ListBuild(x)
                all_lists.append(list_build.build_list())

            all_lists = dumps(all_lists)

            return all_lists, 200
        else:
            abort(404, error="No lists found")

    def post(self, household_id):
        """
        Gets the values from the website and stores the new list items in the database using the household_id

        How post requests for lists should be:
        requests.post(BASE + "shared_list/<int: household_id>", {"name": "some name"})

        :returns
        If successful,
        {'message': 'List Created'}

        if same name exists, returns
        {'error': "List Name Must Be Unique"}
        """
        # Getting values from the website
        connection, cursor = get_conn()
        parser = reqparse.RequestParser()
        parser.add_argument(
            "name",
            type=str,
            help="Name of the list is required",
            required=True,
            location="form",
        )
        parser.add_argument("id", type=int, location="form")
        args = parser.parse_args()
        name = args.get("name")
        list_id = args.get("id")

        cursor.execute(
            "SELECT * FROM list WHERE name = '%s' AND household_id = %s;"
            % (name, household_id)
        )
        list_back = cursor.fetchone()

        id_back = None
        if list_id:
            cursor.execute("SELECT * FROM list WHERE id = %s;" % list_id)
            id_back = cursor.fetchone()

        if list_back:
            abort(409, error="List Name Must Be Unique")
        elif id_back:
            abort(409, error="ID Must Be Unique")
        elif list_id:
            # Query to insert to database
            query = "INSERT INTO list (id, name, household_id) VALUES (%s, '%s', %s);"
            data = (list_id, name, household_id)

            cursor.execute(query % data)
            connection.commit()
            return {"message": "List Created"}, 201
        else:
            query = "INSERT INTO list (name, household_id) VALUES ('%s', %s);"
            data = (name, household_id)

            cursor.execute(query % data)
            connection.commit()
            return {"message": "List Created"}, 201


class ListDetails(Resource):
    def delete(self, list_id):
        """
        Delete a full list from the database using the list_id

        How delete requests for lists should be:
        requests.delete(BASE + "list_details/<int: list_id>")

        :returns
        if successful,
        {'message': 'List Deleted'}
        """
        connection, cursor = get_conn()

        cursor.execute("SELECT * FROM list WHERE id = %s;" % list_id)
        present = cursor.fetchone()

        if present is not None:
            query2 = "DELETE FROM list_event WHERE list_event.list = %s;"
            cursor.execute(query2 % list_id)
            connection.commit()

            query1 = "DELETE FROM list WHERE list.id = %s;"
            cursor.execute(query1 % list_id)
            connection.commit()

            return {"message": "List Deleted"}, 200
        else:
            abort(404, error="List Doesnt Exist")

    def patch(self, list_id):
        """
        Changes the name of the list using the list_id

        How patch requests for lists should be:
        requests.patch(BASE + "list_details/<int: list_id>, {"new_name": "Some new name"})

        :returns
        if successful,
        {'message': 'Update Successful'}
        """
        connection, cursor = get_conn()
        parser = reqparse.RequestParser()
        parser.add_argument(
            "new_name",
            type=str,
            help="Name of the list is required",
            required=True,
            location="form",
        )
        args = parser.parse_args()
        new_name = args.get("new_name")

        query1 = "SELECT * FROM list WHERE id = %s"
        cursor.execute(query1 % list_id)
        id_present = cursor.fetchone()

        query_house_id = "SELECT household_id FROM list WHERE id = %s"
        cursor.execute(query_house_id % list_id)
        house_id = cursor.fetchone()[0]
        print(house_id)

        query2 = (
            "SELECT * FROM list WHERE name = '%s' AND id != %s AND household_id = %s"
        )
        cursor.execute(query2 % (new_name, list_id, house_id))
        name_present = cursor.fetchall()

        if not id_present:
            if name_present:
                abort(404, error="List name already exists and id does not exist")
            else:
                abort(404, error="List id does not exist")
        else:
            if name_present:
                abort(409, error="List name already exists")
            else:
                query = "UPDATE list SET name = '%s' WHERE id = %s;"
                data = (new_name, list_id)
                cursor.execute(query % data)
                connection.commit()

                return {"message": "Update Successful"}, 200


class ListEvents(Resource):
    def post(self, list_id):
        """
        Inserts a new row to the list_event table using the list_id

        How post requests for lists should be:
        requests.post(BASE + "list_events/<int: list_id>", {"task_name": "event name",
                                                            "description_of_task": "Event description",
                                                            "added_user_id": 1})
        ** added_user_id is int and the other two are strings

        :returns
        if successful,
        {'message': 'List Event Created'}

        Will return error if the id does not exist
        """
        connection, cursor = get_conn()
        parser = reqparse.RequestParser()
        parser.add_argument("event_id", type=int, location="form")
        parser.add_argument(
            "task_name",
            type=str,
            required=True,
            location="form",
            help="Name of the task is required",
        )
        parser.add_argument(
            "description_of_task",
            type=str,
            required=True,
            location="form",
            help="Description of the task is required",
        )
        parser.add_argument(
            "added_user_id",
            type=int,
            required=True,
            location="form",
            help="User ID is required",
        )
        args = parser.parse_args()
        event_id = args.get("event_id")
        task_name = args.get("task_name")
        description_of_task = args.get("description_of_task")
        added_user_id = args.get("added_user_id")

        if event_id:
            query1 = "SELECT * FROM list_event WHERE id = %s;"
            cursor.execute(query1 % event_id)
            present = cursor.fetchone()

            if present:
                abort(409, error="Event id already exists")
            else:
                query = (
                    "INSERT INTO list_event (id, task, description, added_by_user, list) "
                    "VALUES (%s, '%s', '%s', %s, %s);"
                )
                data = (
                    event_id,
                    task_name,
                    description_of_task,
                    added_user_id,
                    list_id,
                )
                cursor.execute(query % data)
                connection.commit()
                return {"message": "List Event Created"}, 201

        else:
            cursor = connection.cursor()
            # Query to insert to database
            query = "INSERT INTO list_event (task, description, added_by_user, list) VALUES ('%s', '%s', %s, %s);"
            data = (task_name, description_of_task, added_user_id, list_id)
            print(data)
            cursor.execute(query % data)
            connection.commit()
            return {"message": "List Event Created"}, 201

    def get(self, list_id):
        """
        Returns all the events under a list using the list_id

        How get requests for list evemts should be:
        requests.get(BASE + "list_events/<int: list_id>")

        :returns
        The server will return following json object:
        {
            [{list_event1}, {list_event2}, {list_event3}]
        }

        The list event has the following structure:
        {
        'id': 3,
        'task_name': 'name1',
        'description_of_task': 'description1',
        'added_user_id': 1,
        'checked_off_by_user': None,
        'list': 1,
        }

        If nothing is found, it will return error message
        """
        cursor = get_db()
        query = "SELECT * FROM list_event WHERE list = %s;"
        cursor.execute(query % list_id)
        fetched_result = cursor.fetchall()

        list_events = []
        if fetched_result:
            for x in fetched_result:
                event_objects = ListEventBuild(x)
                list_events.append(event_objects.build_list_event())

            list_events = dumps(list_events)

            return list_events, 200
        else:
            abort(404, error="List id not found")


class ListEventDetails(Resource):
    def delete(self, list_event_id):
        """
        Delete a list event from the database using the list_event_id

        How delete requests for lists should be:
        requests.delete(BASE + "list_event_detail/<int: list_event_id>")

        :returns
        if successful,
        {'message': 'List Event Deleted'}
        """
        connection, cursor = get_conn()
        cursor.execute("SELECT * FROM list_event WHERE id = %s;" % list_event_id)
        present = cursor.fetchone()

        if present:
            query = "DELETE FROM list_event WHERE id = %s;"
            cursor.execute(query % list_event_id)
            connection.commit()
            return {"message": "List Event Deleted"}, 200
        else:
            abort(404, error="List Event Doesnt Exist")

    # Check off list event
    def patch(self, list_event_id):
        """
        Patch a list event from the database using the list_event_id

        How patch requests for lists should be:
        requests.patch(BASE + "list_event_detail/<int: list_event_id>", {"user_id": 4})

        :returns
        if it was null and adds an id,
        {"message": "Checked-off"}

        if opposite,
        {"message": "Un-Checked"}
        """
        connection, cursor = get_conn()
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, location="form")
        args = parser.parse_args()
        user_id = args.get("user_id")

        cursor.execute(
            "SELECT * FROM list_event WHERE id = %s AND checked_off_by_user is NULL;"
            % list_event_id
        )
        check_off = cursor.fetchone()

        if check_off and user_id:
            query = "UPDATE list_event SET checked_off_by_user = %s WHERE id = %s;"
            data = (user_id, list_event_id)
            cursor.execute(query % data)
            connection.commit()
            return {"message": "Checked-off"}, 200

        elif check_off and not user_id:
            abort(406, error="User ID required to check-off")

        elif not check_off:
            query = "UPDATE list_event SET checked_off_by_user = NULL WHERE id = %s;"
            cursor.execute(query % list_event_id)
            connection.commit()
            return {"message": "Un-Checked"}, 200

    def put(self, list_event_id):
        """
        Inserts a new row to the list_event table using the list_id

        How put requests for lists should be:
        requests.put(BASE + "list_events/<int: list_id>", {"task_name": "event name",
                                                            "description_of_task": "Event description",
                                                            "added_user_id": 1})
        ** added_user_id is int and the other two are strings

        :returns
        if successful,
        {'message': 'List Event Created'}

        Will return error if the id does not exist
        """
        connection, cursor = get_conn()
        parser = reqparse.RequestParser()
        parser.add_argument(
            "new_task",
            type=str,
            required=True,
            location="form",
            help="Name of the task is required",
        )
        parser.add_argument(
            "new_description",
            type=str,
            required=True,
            location="form",
            help="Description of the task is required",
        )
        args = parser.parse_args()
        new_task = args.get("new_task")
        new_description = args.get("new_description")

        cursor.execute("SELECT * FROM list_event WHERE id = %s;" % list_event_id)
        present = cursor.fetchone()

        if present:
            cursor = connection.cursor()
            query = (
                "UPDATE list_event SET task = '%s', description = '%s' WHERE id = %s;"
            )
            data = (new_task, new_description, list_event_id)
            cursor.execute(query % data)
            connection.commit()
            return {"message": "Task details updated"}, 200
        else:
            abort(404, error="Event not found")
