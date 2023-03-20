import datetime
import json
from dataclasses import dataclass

import mysql.connector
import mysql.connector.cursor

from transactions import ledger

class UserError(Exception):
    ...


@dataclass
class User:
    u_id: int
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
    ):
        """Insert self to database"""

        try:
            cur.execute(
                """ INSERT INTO user (first_name, surname, email, password, date_of_birth, household_id, color)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                [v for v in self.__dict__.values()][1:],
            )
        except mysql.connector.errors.IntegrityError:
            # means that email already exists
            raise UserError("User with email {self.email} already exists")

        conn.commit()

    def join_household(
        self,
        house: int,
        cur: mysql.connector.cursor.MySQLCursor,
        conn: mysql.connector.MySQLConnection,
    ):
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

    def leave_household(self, cur: mysql.connector.cursor.MySQLCursor, conn: mysql.connector.MySQLConnection):
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
            cur.execute("""UPDATE user SET household_id = null WHERE email = %s""", [self.email])
            conn.commit()


    def delete(self):
        ...

    @staticmethod
    def build_from_email(email: str):
        ...

    @property
    def json(self):
        return json.dumps(
            {
                "user_id": self.u_id,
                "first_name": self.first_name,
                "surname": self.surname,
                "email": self.email,
                "password": str(self.password, encoding="utf-8"),
                "dob": self.dob.isoformat(),
                "household_id": self.household,
                "colour": self.colour,
            }
        )
