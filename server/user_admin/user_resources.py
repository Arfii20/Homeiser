"""Resources to do with user admin. Here are the resources for:
    Adding, removing, ~modifying~ users
    Adding and removing houses
    Joining and leaving houses"""

from flask_restful import Resource
from flask import request
import json

from admin.user import User, UserError
from server.db_handler import get_conn


class UserResource(Resource):
    def get(self, email: str):
        """return a user given an email"""

        conn, cur = get_conn()

        try:
            u = User.build_from_email(email, cur)
        except UserError as ue:
            # if we fail to build from email, return a 404
            return str(ue), 404

        return u.json, 200

    def post(self):
        """Insert a new user into the table"""

        conn, cur = get_conn()
        r = request.get_json()

        if type(r) is str:
            r = json.loads(r)

        usr = User.build_from_req(request=r)

        try:
            usr.insert_to_database(cur, conn)
        except UserError as ue:
            return str(ue), 500

    def patch(self, household_id: int, email: str, joining: bool):
        """If joining is true, user will try to join household
        If joining is false, user will try to leave household
        """
        conn, cur = get_conn()
        usr = User.build_from_email(email, cur)

        try:
            if joining:
                usr.join_household(household_id, cur, conn)
            else:
                usr.leave_household(cur, conn)
        except UserError as ue:
            return str(ue), 500

        return 200

    def delete(self, email: str):
        """Used to delete a user account"""
        conn, cur = get_conn()
        u = User.build_from_email(email, cur)
        try:
            u.delete(cur, conn)
        except UserError as ue:
            return str(ue), 500

        return f"Deleted user {email}", 200



class House(Resource):
    def post(self):
        """Used to create a household"""

    def delete(self, household_id: int):
        """Used to delete a household given only one person is a member of the house"""
