from __future__ import annotations

import datetime
import hashlib
import json
from dataclasses import dataclass

import mysql.connector
import mysql.connector.cursor
import requests

from transactions import ledger


class UserError(Exception):
    ...


@dataclass
class User:

    """
    JSON Format
     {
            "user_id": int | None,
            "first_name": str,
            "surname": str,
            "email": str,
            "password": bytes,
            "dob": date (isoformat),
            "household_id": int | None,
            "colour": int | None,
        }
    """

    u_id: int | None
    first_name: str
    surname: str
    email: str
    password: bytes
    dob: datetime.date
    household: int | None
    colour: int | None

    def insert_to_database(
        self,
        cur: mysql.connector.cursor.MySQLCursor,
        conn: mysql.connector.MySQLConnection,
    ) -> None:
        """Insert self to database"""

        no_uid_query = """ INSERT INTO user (first_name, surname, email, password, date_of_birth, household_id, color)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);"""

        uid_query = """INSERT INTO user VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""

        try:
            if self.u_id:
                cur.execute(uid_query, [v for v in self.__dict__.values()])
            else:
                cur.execute(no_uid_query, [v for v in self.__dict__.values()][1:])

        except mysql.connector.errors.IntegrityError:
            # means that email already exists
            raise UserError(f"User with email {self.email} already exists")

        conn.commit()

    def join_household(
        self,
        house: int,
        cur: mysql.connector.cursor.MySQLCursor,
        conn: mysql.connector.MySQLConnection,
    ) -> None:
        """Join a household if not already part of one"""

        # check to see if already part of a household
        cur.execute("""SELECT household_id FROM user WHERE email = %s""", [self.email])

        # if part of a household raise an error
        if h_id := cur.fetchone()[0]:
            raise UserError(f"User is already part of household {h_id}")

        # otherwise update db
        cur.execute(
            "UPDATE user SET household_id = %s WHERE email = %s", [house, self.email]
        )
        conn.commit()

    def leave_household(
        self,
        cur: mysql.connector.cursor.MySQLCursor,
        conn: mysql.connector.MySQLConnection,
    ) -> None:
        """Leave a household if
        a. already part of household
        b. no open transactions in group"""

        # check to see if part of a household
        cur.execute("""SELECT household_id FROM user WHERE email = %s""", [self.email])

        if (h_id := cur.fetchone()[0]) is None:
            raise UserError(f"User {self.email} is already part of household {h_id})")

        # pull u_id if it is 0
        if not self.u_id:
            cur.execute("""SELECT id FROM user WHERE email = %s""", [self.email])
            self.u_id = cur.fetchone()[0]

        # check for open transactions
        # when a ledger is built it raises EmptyLedger where user involved in no transactions
        # hence if we build successfully then raise a UserError, saying that this user is involved in transactions
        # and thus cannot leave the house.

        # otherwise, handle empty ledger by proceeding with leaving the house
        try:
            ledger.Ledger.build_from_user_id(self.u_id, cur)
            raise UserError(f"User {self.email} is involved in transactions")

        except ledger.EmptyLedger:
            # update db with new household id having passed both checks
            cur.execute(
                """UPDATE user SET household_id = null WHERE email = %s""", [self.email]
            )
            conn.commit()

    def delete(
        self,
        cur: mysql.connector.cursor.MySQLCursor,
        conn: mysql.connector.MySQLConnection,
    ) -> None:
        """Only let user delete their account if they are not involved in a household"""
        # check to see if part of a household
        cur.execute("""SELECT household_id FROM user WHERE email = %s""", [self.email])
        if h_id := cur.fetchone():
            raise UserError(
                f"Cannot delete account as you are still part of household {h_id[0]}"
            )

        # pull u_id if it is 0
        if not self.u_id:
            cur.execute("""SELECT id FROM user WHERE email = %s""", [self.email])
            self.u_id = cur.fetchone()[0]

        # delete all transactions which user was involved in
        cur.execute(
            """SELECT id FROM pairs WHERE src = %s OR dest = %s""", 2 * [self.u_id]
        )
        pair_ids = cur.fetchall()

        for pair_id in pair_ids:
            cur.execute("""DELETE FROM transaction WHERE pair_id = %s""", [pair_id[0]])

        conn.commit()

        # delete all pairs which the user was involved in
        for pair_id in pair_ids:
            cur.execute("""DELETE FROM pairs WHERE id = %s""", [pair_id[0]])

        # now all fks have been deleted - delete user
        cur.execute("""DELETE FROM user WHERE id = %s""", [self.u_id])
        conn.commit()

    @staticmethod
    def build_from_email(email: str, cur: mysql.connector.cursor.MySQLCursor) -> User:
        cur.execute("""SELECT * FROM user WHERE email = %s""", [email])
        attrs = cur.fetchall()

        if attrs:
            attrs = attrs[0]
        else:
            raise UserError(f"No user with the email {email}")

        # swap password and email field to fit with database column order
        attrs = attrs[:3] + (attrs[4], bytes(attrs[3], encoding="utf-8")) + attrs[5:]

        return User(*attrs)

    @staticmethod
    def build_from_req(*, request: requests.Response | dict) -> User:
        # load json representation of User into a dict if it is not already a dict
        if type(request) != dict:
            r = json.loads(request.json())  # type: ignore
        else:
            r = request

        # initialise hasher
        hasher = hashlib.sha3_256()

        try:
            passwd = r["password"]
        except KeyError as ke:
            raise UserError(ke)

        print(passwd)
        hasher.update(bytes(passwd, encoding = 'utf-8'))
        user = User(*r.values())
        user.password = str(hasher.digest())

        return user

    @property
    def json(self):
        return json.dumps(
            {
                "user_id": self.u_id,
                "first_name": self.first_name,
                "surname": self.surname,
                "email": self.email,
                "password": self.password,
                "dob": self.dob.isoformat()
                if type(self.dob) is datetime.date
                else self.dob,
                "household_id": self.household,
                "colour": self.colour,
            }
        )
