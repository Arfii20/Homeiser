import hashlib

from flask_restful import Resource, reqparse, abort
from server.db_handler import get_conn, get_db

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
        Sends the new data to the database
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

        hasher = hashlib.sha3_256()
        hasher.update(bytes(password, encoding='utf8'))
        exp_password = str(hasher.digest())

        query_for_id = """SELECT password FROM user WHERE id = %s"""
        cursor.execute(query_for_id % user_id)
        real_password = cursor.fetchall()

        if exp_password == real_password[0][0]:
            return {"message": "User Updated"}
        else:
            abort(404, error="User not found")

    def delete(self, user_id):
        """
        Delete user activies if someone leaves the house
        :return:
        """
        connection, cursor = get_conn()
        try:
            # Get all calendar events the user was involved in
            cursor.execute(
                """SELECT calendar_event_id FROM user_doing_calendar_event WHERE added_by_user = %s""", [user_id]
            )
            calendar_ids = cursor.fetchall()

            if calendar_ids:
                cursor.execute("""DELETE FROM user_doing_calendar_event WHERE user_id = %s OR added_by_user = %s""", 2 * [user_id])
                connection.commit()

                for ids in calendar_ids:
                    cursor.execute("""DELETE FROM calendar_event WHERE id = %s""", [ids[0]])
                    connection.commit()

            # Get all list events the user was involved in
            cursor.execute(
                """SELECT id, list FROM list_event WHERE added_by_user = %s""", [user_id]
            )
            list_ids = cursor.fetchall()

            # Delete list events
            if list_ids:
                for idl in list_ids:
                    cursor.execute("""DELETE FROM list_event WHERE id = %s""", [idl[0]])
                    connection.commit()

            return {"message": "Everything Deleted"}, 201
        except:
            return {"message": "Error deleting stuff"}, 500


class GroupDetails(Resource):
    def get(self, house_id):
        """
        Sends the group details to the website
        requests.get(BASE + "group_details/<int:house_id>")

        :returns:
        The server will return a json object of user
        """
        cursor = get_db()
        obj = {}
        users = []

        query_for_house_name = "SELECT id, name FROM household WHERE id = %s;"
        cursor.execute(query_for_house_name % house_id)

        result_house = cursor.fetchall()

        if result_house:
            for x in result_house:
                obj["id"] = x[0]
                obj["house_name"] = x[1]

            query_for_users = "SELECT first_name, surname FROM user WHERE household_id = %s;"
            cursor.execute(query_for_users % house_id)
            result = cursor.fetchall()

            for x in result:
                users.append(x[0] + " " + x[1])

            obj["users"] = users

            return obj, 200
        else:
            abort(404, error="Household id not found")
