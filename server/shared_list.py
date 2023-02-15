"""
The shared list methods are defined here
"""

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from mysql.connector import connect, Error
import json

app = Flask(__name__)
api = Api(app)


def get_db():
    connection = connect(
        host="localhost",
        user="root",
        password="Arfi12000@",
        database="x5db"
    )
    return connection


print(get_db())


class SharedList(Resource):
    def __init__(self):
        pass

    @app.route('/new_list', method="POST")
    def new_list(self):
        """
        Gets the values from the website and stores the new list items in the database
        """
        # Getting values from the website
        name = request.form.get("name")
        user_id = current_user.household_id  # <----------------------------------------------

        cursor = get_db().cursor()

        # Querying for house_id
        houseid_query = "SELECT household_id FROM user WHERE id = ?"
        houseid = cursor.execute(houseid_query, [user_id])

        # Query to insert to database
        query = "INSERT INTO list (name, household_id) VALUES (?, ?);"

        cursor.execute(query, [name], [houseid])

        return  # render_template("name") # <----------------------------------------------

    @app.route('/delete_list', method="POST")
    def delete_list(self):
        """
        Delete a full list from the database
        :return: name of the person who deleted the list
        """
        list_in = json.loads(request.data)
        list_in_id = list_in["list_id"]

        cursor = get_db().cursor()

        query = "DELETE FROM list, list_event WHERE list.id = ? and list_event.list = ?;"
        cursor.execute(query, [list_in_id], [list_in_id])

        return jsonify({})  # <----------------------------------------------

    @app.route('/update_list', methods="POST")
    def change_list_name(self):
        """
        Changes the name of the list name and returns the new name
        :return: new name of the list
        """
        new_name = request.form.get("name")
        list_id = request.form.get("list_id")  # <----------------------------------------------
        cursor = get_db().cursor()

        query = "UPDATE FROM list SET name = ? WHERE id = ?;"
        cursor.execute(query, [new_name], [list_id])

        return  # render_template("name") # <----------------------------------------------

    # @app.route('/shared_lists', method="GET")
    # def show_list_names(self):
    #     """
    #     Sends all the list names to the website
    #     :return: all list names
    #     """
    #     cursor = get_db().cursor()
    #
    #     name = cursor.execute("SELECT name FROM list WHERe id = listID;")
    #
    #     return name


class ListEvents(Resource):

    def __init__(self):
        pass

    @app.route('/list_event', method="POST")
    def new_list_event(self):
        """
        Inserts a new row to the list_event table
        :return: sends the new row to the website
        """
        # Getting values from the website
        task_name = request.form.get("task_name")
        description_of_task = request.form.get("task_description")
        added_user_id = current_user.id  # <----------------------------------------------
        list_id = request.form.get("list_id")  # <----------------------------------------------

        cursor = get_db().cursor()

        # Query to insert to database
        query = "INSERT INTO list_event (task, description, added_by_user, list) VALUES (?, ?, ?, ?);"

        cursor.execute(query, [task_name], [description_of_task], [added_user_id], [list_id])

        return  # render_template("name of list page")  <---------------------------------------------------

    @app.route('/delete_list_event', method="POST")
    def delete_list_event(self):
        """
        Deletes a row from the list
        :return: jsonify({})
        """
        event_in = json.loads(request.data)
        event_in_id = event_in["list_event_id"]

        cursor = get_db().cursor()

        query = "DELETE FROM list_event WHERE id = ?;"
        cursor.execute(query, [event_in_id])

        return jsonify({})  # <----------------------------------------------

    @app.route('/checkoff_list_event', method="POST")
    def check_off_list_event(self):
        """
        Checks off an event
        :return: jsonify({})
        """
        user_id = current_user.id  # <----------------------------------------------

        cursor = get_db().cursor()

        checked_off = cursor.execute("SELECT checked_off_by_user FROM list_event WHERE list = ?;", [user_id])

        # If checked_off is not null
        if checked_off:
            query = "UPDATE list_event SET checked_off_by_user = null WHERE id = ?;"
            value = None
            cursor.execute(query, [value])

        # If checked_off is null
        else:
            query = "DELETE FROM list_event WHERE id = ?;"
            cursor.execute(query, [user_id])

        return jsonify({})  # <----------------------------------------------

    @app.route('/update_list_event', method="POST")
    def update_list_event(self):
        """
        For Updating Something in the list
        :return:
        """
        new_task = request.form.get("task_name")
        new_description = request.form.get("task_description")
        list_id = request.form.get("list_id")  # <----------------------------------------------

        cursor = get_db().cursor()

        query = "SET task = ?, description = ? WHERE id = ?;"
        cursor.execute(query, [new_task], [new_description], [list_id])

        return  # render_template("name of list page")  <---------------------------------------------------

    # @app.route('/shared_lists', methods=["GET", "POST"])
    # def show_list_event(self):
    #     """
    #     Shows the list events for a particular list
    #     :return:
    #     """
    #     # # For sending the tasks to the server
    #     # SELECT * FROM list_event WHERE list = listID;


api.add_resource(SharedList, "/shared_list/<int:id>")
api.add_resource(ListEvents, "/list_events/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
