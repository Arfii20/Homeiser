"""
The shared list methods are defined here
"""

from flask import Flask
from flask_restful import Resource, Api, reqparse
from mysql.connector import connect

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
        args = parser.parse_args()
        name = args.get("name")

        cursor1 = connection.cursor()
        cursor1.execute("SELECT * FROM list WHERE name = '%s';" % name)
        list_back = cursor1.fetchone()

        if list_back is not None:
            return {"Response": "ListNameMustBeUnique"}, 291
        else:
            # Query to insert to database
            query = "INSERT INTO list (name, household_id) VALUES ('%s', %s);"
            data = (name, household_id)

            cursor = connection.cursor()
            cursor.execute(query % data)
            connection.commit()

            return {"Response": "ListCreated"}, 292

    def get(self, household_id):
        """
        Sends all the list names to the website
        :return: all list names
        """
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM list WHERE household_id = %s;" % household_id)

        objects = []
        for x in cursor.fetchall():
            print(x)
            objects.append(x)

        return {"Response": "Works"}, 293  # <-------------------------------------------------------


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
            return {'Response': 'ListDeleted'}, 294
        else:
            return {'Response': 'ListDoesntExist'}, 295

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

        query = "UPDATE list SET name = '%s' WHERE id = %s;"
        data = (new_name, list_id)

        cursor = connection.cursor()
        cursor.execute(query % data)
        connection.commit()

        return {'Response': 'UpdateSuccessful'}, 296


class ListEvents(Resource):

    # Add mew list event
    def post(self, list_id):
        """
        Inserts a new row to the list_event table
        :return: sends the new row to the website
        """
        print("Hello")
        parser = reqparse.RequestParser()
        parser.add_argument("task_name", type=str, required=True, location="form",
                            help="Name of the task is required")
        parser.add_argument("description_of_task", type=str, required=True,
                            location="form", help="Description of the task is required")
        parser.add_argument("added_user_id", type=int, required=True,
                            location="form", help="User ID is required")
        args = parser.parse_args()
        task_name = args.get("task_name")
        description_of_task = args.get("description_of_task")
        added_user_id = args.get("added_user_id")

        cursor1 = connection.cursor()
        query1 = "SELECT * FROM list_event WHERE (task = '%s' AND checked_off_by_user is NOT NULL);"
        cursor1.execute(query1 % task_name)
        present = cursor1.fetchone()

        if present is not None:
            cursor = connection.cursor()

            # Query to insert to database
            query = "INSERT INTO list_event (task, description, added_by_user, list) VALUES ('%s', '%s', %s, %s);"
            data = (task_name, description_of_task, added_user_id, list_id)
            cursor.execute(query % data)
            connection.commit()
            return {"Response": "ListEventCreated"}, 281
        else:
            return {"Response": "ListEventAlreadyExists"}, 282

    def get(self, list_id):
        """
        Shows the list events for a particular list
        :return:
        """
        cursor = connection.cursor()
        query = "SELECT * FROM list_event WHERE list = %s;"
        cursor.execute(query % list_id)

        objects = []
        for x in cursor.fetchall():
            objects.append(x)
            print(x)

        return {"Response": "Works"}, 283  # <-------------------------------------------------------


class ListEventDetails(Resource):

    def delete(self, list_event_id):
        """
        Deletes a row from the list
        :return: jsonify({})
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM list_event WHERE id = %s;" % list_event_id)
        present = cursor.fetchone()

        if present is not None:
            query = "DELETE FROM list_event WHERE id = %s;"
            cursor1 = connection.cursor()
            cursor1.execute(query % list_event_id)
            connection.commit()
            return {'Response': 'ListEventDeleted'}, 284
        else:
            return {'Response': 'ListEventDoesntExist'}, 285

    # Check off list event
    def patch(self, list_event_id):
        """
        Checks off an event
        :return: jsonify({})
        """
        parser = reqparse.RequestParser()
        parser.add_argument("user_id", type=str, required=True, location="form",
                            help="User ID required. Yes even for unchecking")
        args = parser.parse_args()
        user_id = args.get("user_id")

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM list_event WHERE id = %s AND checked_off_by_user is NULL;" % list_event_id)
        checked_off = cursor.fetchone()

        # If checked_off is null
        if checked_off is not None:
            query = "UPDATE list_event SET checked_off_by_user = %s WHERE id = %s;"
            data = (user_id, list_event_id)
            cursor.execute(query % data)
            connection.commit()
            return {"Response": "Checked-off"}, 286
            # If checked_off is not null
        elif checked_off is None:
            query = "UPDATE list_event SET checked_off_by_user = NULL WHERE id = %s;"
            cursor.execute(query % list_event_id)
            connection.commit()
            return {"Response": "Un-Checked"}, 287

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

        query = "UPDATE list_event SET task = '%s', description = '%s' WHERE id = %s;"
        data = (new_task, new_description, list_event_id)
        cursor.execute(query % data)
        connection.commit()

        return {"Response": "Task details updated"}, 288


api.add_resource(SharedList, "/shared_list/<int:household_id>")
api.add_resource(ListDetails, "/list_details/<int:list_id>")
api.add_resource(ListEvents, "/list_events/<int:list_id>")
api.add_resource(ListEventDetails, "/list_event_details/<int:list_event_id>")

if __name__ == '__main__':
    app.run(debug=True)
