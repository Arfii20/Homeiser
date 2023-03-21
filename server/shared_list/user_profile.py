from flask_restful import Resource, reqparse, abort
from server.db_handler import get_conn, get_db
from json import dumps
import re

class UserProfile(Resource):
    def get(self, user_id):
        """
        Sends the colours assigned to individual users to the website
        How get requests for user_colours should be like:
        requests.get(BASE + "user_profile/<int:user_id>")

        :returns:
        The server will return following json object:
        {
        'id':
        'color':
        }
        """
        cursor = get_db()
        query = "SELECT first_name, surname, email, date_of_birth FROM user WHERE user_id = %s;"
        cursor.execute(query % user_id)

        result = cursor.fetchall()

        obj = {}
        if result:
            for x in result:
                obj.first_name = x[0]
                obj.surname = x[1]
                obj.email = x[2]
                obj.date_of_birth = x[3]
            return obj, 200
        else:
            abort(404, error="Users or household id not found")