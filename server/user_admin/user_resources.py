"""Resources to do with user admin. Here are the resources for:
    Adding, removing, ~modifying~ users
    Adding and removing houses
    Joining and leaving houses"""

from flask_restful import Resource
from flask import request
import hashlib
import json

from admin.house import (
    House,
    HouseConstructionError,
    HouseInsertionError,
    HouseDeletionError,
)
from admin.user import User, UserError
from server.db_handler import get_conn


class UserLoginResource(Resource):

    def post(self):
        """Return json for a user given an email and password;
        accept requests in the form
        {'email': str,
         'password': str}

         (password in plaintext)
         """

        details = request.get_json()

        hasher = hashlib.sha3_256()
        hasher.update(bytes(details['password'], encoding='utf8'))

        exp_password = str(hasher.digest())
        _, cur = get_conn()

        try:
            u = User.build_from_email(details['email'], cur)
        except UserError as ue:
            # if we fail to build from email, return a 404
            return str(ue), 404

        if bytes(exp_password, encoding='utf8') == u.password:
            return u.json, 200
        else:
            return 'Incorrect Password', 401


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

        return usr.json, 201

    def patch(self, household_id: int, email: str, joining: int):
        """If joining is true (non-zero), user will try to join household
        If joining is false (0), user will try to leave household
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

        usr = User.build_from_email(email, cur)
        return usr.json, 200

    def delete(self, email: str):
        """Used to delete a user account"""
        conn, cur = get_conn()
        u = User.build_from_email(email, cur)
        try:
            u.delete(cur, conn)
        except UserError as ue:
            return str(ue), 500

        return f"Deleted user {email}", 200


class HouseResource(Resource):
    def get(self, household_id: int):
        """Get group info"""

        conn, _ = get_conn()

        try:
            house = House.build_from_id(household_id, conn)
        except HouseConstructionError as hce:
            # error means that id wasn't found in server
            return str(hce), 404

        return house.json, 200

    def post(self):
        """Used to create a household"""

        conn, _ = get_conn()

        # try to build a house from request
        try:
            house = House.build_from_request(request=request)
        except HouseConstructionError as hce:
            return str(hce), 500

        # try to insert the house into the db
        try:
            house.insert_to_db(conn)
        except HouseInsertionError as hie:
            return str(hie), 500

        # if successful return the created house and a 201
        return house.json, 201

    def delete(self, household_id: int):
        """Used to delete a household given only one person is a member of the house"""

        conn, _ = get_conn()

        # try to build a house from id
        try:
            house = House.build_from_id(household_id, conn)
        except HouseConstructionError as hce:
            # error means that id wasn't found in server
            return str(hce), 404

        # try to delete
        try:
            house.delete(conn)
        except HouseDeletionError as hde:
            return str(hde), 500
