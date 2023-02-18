"""
The shared list methods are defined here
"""

from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort
from mysql.connector import connect
from server.host import *

# with app.app_context():
#     connection = get_db("Arfi12000@")

connection = connect(
    host="localhost",
    user="root",
    password="Arfi12000@",
    database="x5db",
    buffered=True
)


# return connection
# print(get_db())


class SharedList(Resource):
    # Make new list
    def post(self, household_id):
        """
        Gets the values from the website and stores the new list items in the database
        """
        # Getting values from the website
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, help='Name of the list is required',
                            required=True, location='form')
        parser.add_argument('id', type=int, location='form')
        args = parser.parse_args()
        name = args.get("name")
        list_id = args.get("id")

        cursor1 = connection.cursor()
        cursor1.execute("SELECT * FROM list WHERE name = '%s';" % name)
        list_back = cursor1.fetchone()

        id_back = None

        if list_id:
            cursor2 = connection.cursor()
            cursor2.execute("SELECT * FROM list WHERE id = %s;" % list_id)
            id_back = cursor2.fetchone()

        if list_back:
            abort(406, Error="List Name Must Be Unique")
        elif id_back:
            abort(406, Error="ID Must Be Unique")
        elif list_id:
            # Query to insert to database
            query = "INSERT INTO list (id, name, household_id) VALUES (%s, '%s', %s);"
            data = (list_id, name, household_id)

            cursor = connection.cursor()
            cursor.execute(query % data)
            connection.commit()
            return {"message": "List Created"}, 201
        else:
            query = "INSERT INTO list (name, household_id) VALUES ('%s', %s);"
            data = (name, household_id)

            cursor = connection.cursor()
            cursor.execute(query % data)
            connection.commit()
            return {"message": "List Created"}, 201

    def get(self, household_id):
        """
        Sends all the list names to the website
        :return: all list names
        """
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM list WHERE household_id = %s;" % household_id)

        objects = {
            "id": [],
            "name": [],
            "household_id": []
        }
        for x in cursor.fetchall():
            objects["id"].append(x[0])
            objects["name"].append(x[1])
            objects["household_id"].append(x[2])

        return objects, 202


class ListDetails(Resource):

    def delete(self, list_id):
        """
        Delete a full list from the database
        :return: name of the person who deleted the list
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM list WHERE id = %s;" % list_id)
        present = cursor.fetchone()

        if present is not None:
            query1 = "DELETE FROM list WHERE list.id = %s;"
            cursor1 = connection.cursor()
            cursor1.execute(query1 % list_id)
            connection.commit()

            query2 = "DELETE FROM list_event WHERE list_event.list = %s;"
            cursor2 = connection.cursor()
            cursor2.execute(query2 % list_id)
            connection.commit()
            return {'message': 'List Deleted'}, 202
        else:
            return {'message': 'List Doesnt Exist'}, 404

    def patch(self, list_id):
        """
        Changes the name of the list name and returns the new name
        :return: new name of the list
        """
        parser = reqparse.RequestParser()
        parser.add_argument('new_name', type=str, help='Name of the list is required',
                            required=True, location='form')
        args = parser.parse_args()
        new_name = args.get("new_name")

        cursor1 = connection.cursor()
        query1 = "SELECT * FROM list WHERE id = %s"
        cursor1.execute(query1 % list_id)
        id_present = cursor1.fetchone()

        cursor2 = connection.cursor()
        query2 = "SELECT * FROM list WHERE name = '%s' AND id != %s"
        cursor2.execute(query2 % (new_name, list_id))
        name_present = cursor2.fetchall()

        if not id_present:
            if name_present:
                abort(404, error="List name already exists and id does not exist")
            else:
                abort(404, error="List id does not exist")
        else:
            if name_present:
                abort(406, error="List name already exists")
            else:
                query = "UPDATE list SET name = '%s' WHERE id = %s;"
                data = (new_name, list_id)

                cursor = connection.cursor()
                cursor.execute(query % data)
                connection.commit()

                return {'message': 'Update Successful'}, 202


class ListEvents(Resource):

    def post(self, list_id):
        """
        Inserts a new row to the list_event table
        :return: sends the new row to the website
        """
        parser = reqparse.RequestParser()
        parser.add_argument("event_id", type=int, location="form")        
        parser.add_argument("task_name", type=str, required=True, location="form",
                            help="Name of the task is required")
        parser.add_argument("description_of_task", type=str, required=True,
                            location="form", help="Description of the task is required")
        parser.add_argument("added_user_id", type=int, required=True,
                            location="form", help="User ID is required")
        args = parser.parse_args()
        event_id = args.get("event_id")
        task_name = args.get("task_name")
        description_of_task = args.get("description_of_task")
        added_user_id = args.get("added_user_id")
        
        if event_id:
            cursor1 = connection.cursor()
            query1 = "SELECT * FROM list_event WHERE id = %s;"
            cursor1.execute(query1 % event_id)
            present = cursor1.fetchone()
    
            if present:
                abort(406, error="Event id already exists")
            else:
                cursor = connection.cursor()
                query = "INSERT INTO list_event (id, task, description, added_by_user, list) " \
                        "VALUES (%s, '%s', '%s', %s, %s);"
                data = (event_id, task_name, description_of_task, added_user_id, list_id)
                cursor.execute(query % data)
                connection.commit()
                return {"message": "List Event Created"}, 201

        else:
            cursor = connection.cursor()
            # Query to insert to database
            query = "INSERT INTO list_event (task, description, added_by_user, list) VALUES ('%s', '%s', %s, %s);"
            data = (task_name, description_of_task, added_user_id, list_id)
            cursor.execute(query % data)
            connection.commit()
            return {"message": "List Event Created"}, 201

    def get(self, list_id):
        """
        Shows the list events for a particular list
        """
        cursor = connection.cursor()
        query = "SELECT * FROM list_event WHERE list = %s;"
        cursor.execute(query % list_id)

        objects = {
            "id": [],
            "task_name": [],
            "description_of_task": [],
            "added_user_id": [],
            "checked_off_by_user": [],
            "list": []
        }
        for x in cursor.fetchall():
            objects["id"].append(x[0])
            objects["task_name"].append(x[1])
            objects["description_of_task"].append(x[2])
            objects["added_user_id"].append(x[3])
            objects["checked_off_by_user"].append(x[4])
            objects["list"].append(x[5])

        if not objects["id"]:
            abort(404, error="List id not found")
        else:
            return objects, 202


class ListEventDetails(Resource):

    def delete(self, list_event_id):
        """
        Deletes a row from the list
        :return: jsonify({})
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM list_event WHERE id = %s;" % list_event_id)
        present = cursor.fetchone()

        if present:
            query = "DELETE FROM list_event WHERE id = %s;"
            cursor1 = connection.cursor()
            cursor1.execute(query % list_event_id)
            connection.commit()
            return {'message': 'List Event Deleted'}, 202
        else:
            return {'message': 'List Event Doesnt Exist'}, 404

    # Check off list event
    def patch(self, list_event_id):
        """
        Checks off an event
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=int, location="form")
        args = parser.parse_args()
        user_id = args.get("user_id")

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM list_event WHERE id = %s AND checked_off_by_user is NULL;" % list_event_id)
        check_off = cursor.fetchone()

        if check_off and user_id:
            query = "UPDATE list_event SET checked_off_by_user = %s WHERE id = %s;"
            data = (user_id, list_event_id)
            cursor.execute(query % data)
            connection.commit()
            return {"message": "Checked-off"}, 202

        elif check_off and not user_id:
            abort(406, error="User ID required to check-off")

        elif not check_off:
            query = "UPDATE list_event SET checked_off_by_user = NULL WHERE id = %s;"
            cursor.execute(query % list_event_id)
            connection.commit()
            return {"message": "Un-Checked"}, 202

    def put(self, list_event_id):
        """
        For Updating Something in the list
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument("new_task", type=str, required=True, location="form",
                            help="Name of the task is required")
        parser.add_argument("new_description", type=str, required=True,
                            location="form", help="Description of the task is required")
        args = parser.parse_args()
        new_task = args.get("new_task")
        new_description = args.get("new_description")

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM list_event WHERE id = %s;" % list_event_id)
        present = cursor.fetchone()

        if present:
            cursor = connection.cursor()
            query = "UPDATE list_event SET task = '%s', description = '%s' WHERE id = %s;"
            data = (new_task, new_description, list_event_id)
            cursor.execute(query % data)
            connection.commit()
            return {"message": "Task details updated"}, 202
        else:
            abort(404, error="Event not found")


api.add_resource(SharedList, "/shared_list/<int:household_id>")
api.add_resource(ListDetails, "/list_details/<int:list_id>")
api.add_resource(ListEvents, "/list_events/<int:list_id>")
api.add_resource(ListEventDetails, "/list_event_details/<int:list_event_id>")

if __name__ == '__main__':
    app.run(debug=True)
