from flask_restful import Resource, reqparse, abort
from server.db_handler import get_conn, get_db
import re

class UserProfile(Resource):
    def get(self, user_id):
        """
        Sends the colours assigned to individual users to the website
        How get requests for user_colours should be like:
        requests.get(BASE + "user_profile/<int:user_id>")

        :returns:
        The server will return a json object of user
        """
        cursor = get_db()
        query = "SELECT first_name, surname, email, date_of_birth FROM user WHERE id = %s;"
        cursor.execute(query % user_id)

        result = cursor.fetchall()

        obj = {}
        if result:
            for x in result:
                obj["first_name"] = x[0]
                obj["surname"] = x[1]
                obj["email"] = x[2]
                obj["date_of_birth"] = x[3].isoformat()
            return obj, 200
        else:
            abort(404, error="Users or household id not found")

    def post(self, user_id):
        """
        Sends the colours assigned to individual users to the website
        How get requests for user_colours should be like:
        requests.post(BASE + "user_profile/<int:user_id>", {first_name: first_name,
                                                        surname: surname,
                                                        email: email,
                                                        date_of_birth})

        :returns:
        The server will return a json object of user
        """
        connection, cursor = get_conn()
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, location="form")
        parser.add_argument(
            "first_name",
            type=str,
            required=True,
            location="form",
            help="First name is required",
        )
        parser.add_argument(
            "surname",
            type=str,
            required=True,
            location="form",
            help="Surname is required",
        )
        parser.add_argument(
            "email",
            type=str,
            required=True,
            location="form",
            help="email is required",
        )
        parser.add_argument(
            "date_of_birth",
            type=str,
            required=True,
            location="form",
            help="Date of birth is required",
        )

        args = parser.parse_args()
        first_name = args.get("first_name")
        surname = args.get("surname")
        email = args.get("email")
        date_of_birth = args.get("date_of_birth")

        query_for_id = """SELECT id FROM user WHERE id = %s """
        cursor.execute(query_for_id % user_id)

        id_exists = cursor.fetchall()

        if id_exists:
            query = "UPDATE user " \
                    "SET " \
                    "first_name = '%s', " \
                    "surname = '%s'," \
                    "email = '%s', " \
                    "date_of_birth = '%s'" \
                    "WHERE id = %s;"

            data = (first_name, surname, email, date_of_birth, user_id)
            cursor.execute(query % data)
            connection.commit()

            return {"message": "User Updated"}
        else:
            abort(404, error="User not found")

    def patch(self, user_id):
        """
                Sends the colours assigned to individual users to the website
                How get requests for user_colours should be like:
                requests.patch(BASE + "user_profile/<int:user_id>", {password: pass})

                :returns:
                The server will return a json object of user
                """
        connection, cursor = get_conn()
        parser = reqparse.RequestParser()
        parser.add_argument("id", type=int, location="form")
        parser.add_argument(
            "password",
            type=str,
            required=True,
            location="form",
            help="Password is required",
        )

        args = parser.parse_args()
        password = args.get("password")

        query_for_id = """SELECT id FROM user WHERE id = %s AND password = '%s'"""
        cursor.execute(query_for_id % (user_id, password))

        id_exists = cursor.fetchall()
        if id_exists:
            return {"message": "User Updated"}
        else:
            abort(404, error="User not found")