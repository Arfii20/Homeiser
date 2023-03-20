import datetime
import json
from dataclasses import dataclass

import mysql.connector
import mysql.connector.cursor


class UserError(Exception): ...


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

    def insert_to_database(self, cur: mysql.connector.cursor.MySQLCursor, conn: mysql.connector.MySQLConnection):
        """Insert self to database"""

        try:
            cur.execute(""" INSERT INTO user (first_name, surname, email, password, date_of_birth, household_id, color)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);""", [v for v in self.__dict__.values()][1:])
        except mysql.connector.errors.IntegrityError:
            # means that email already exists
            raise UserError("User with email {self.email} already exists")

        conn.commit()

    def join_household(self, house: int, cur: mysql.connector.cursor.MySQLCursor):
        """Join a household if not already part of one"""

        # check to see if already part of a household
        cur.execute("""SELECT household_id FROM user WHERE email = %s""", [self.email])

        # if not update household_id with new id; otherwise raise error


    def leave_household(self, house: int):
        ...

    def delete(self):
        ...

    @staticmethod
    def build_from_email(email: str):
        ...

    @staticmethod
    def build_from_id(u_id: int):
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
