from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Request
    from mysql.connector import MySQLConnection
    from mysql.connector.cursor import MySQLCursor


class HouseConstructionError(Exception):
    ...


class HouseInsertionError(Exception):
    ...


class HouseDeletionError(Exception):
    ...


@dataclass
class House:

    """JSON format
    {
    h_id: int  -- if creating a household can leave as null
    name: str
    password: bytes -- transmit in plaintext; server will always send back empty str
    max_residents: int
    road_name: str
    postcode: str

    }
    """

    h_id: int
    name: str
    password: bytes
    max_residents: int
    road_name: str
    postcode: str

    @property
    def json(self):
        """Return each attribute of the object without the password hash"""
        attrs = self.__dict__
        attrs["password"] = ""
        return json.dumps(attrs)

    @staticmethod
    def build_from_request(*, request: Request | dict) -> House:
        """Hashes password upon building"""

        # initialise hasher
        hasher = hashlib.sha3_256()

        # load json representation of Transaction into a dict if it is not already a dict
        if type(request) != dict:
            r: dict = json.loads(request.json())  # type: ignore
        else:
            r = request

        try:
            # clean data, convert into format from request s.th. we can build into a House

            # deal with event that h_id was transmitted with null value
            if type(r["h_id"]) is None:
                r["h_id"] = 0

            # strip whitespace from the postcode, road_name; also capitalise
            r["postcode"] = r["postcode"].replace(" ", "").upper()
            r["road_name"] = r["road_name"].upper()

            # hashing logic

            # encode password as a byte string using utf8 encoding
            r["password"] = bytes(r["password"], encoding="utf8")
            hasher.update(r["password"])
            r["password"] = hasher.digest()

        except KeyError as ke:
            # means that json was not in correct format
            raise HouseConstructionError(ke)

        return House(*r.values())

    @staticmethod
    def build_from_id(h_id: int, conn: MySQLConnection) -> House:
        """Build a house object from database given an id"""
        cur = conn.cursor()

        cur.execute(
            """SELECT household.id, name, password, max_residents, road_name, code FROM household
        JOIN postcode p on household.postcode_id = p.id WHERE household.id = %s""",
            [h_id],
        )

        house_params = cur.fetchone()

        if house_params is None:
            raise HouseConstructionError(f"No house with id {h_id} exists")

        return House(*house_params)

    def insert_to_db(self, conn: MySQLConnection):
        """Inserts the house into the database"""

        cur: MySQLCursor = conn.cursor()

        # if id is provided and already exists raise an error
        if self.h_id:
            cur.execute(
                f"""SELECT count(id) FROM household WHERE id = %s""", [self.h_id]
            )
            if cur.fetchone()[0]:
                raise HouseInsertionError(f"House with id {self.h_id} already exists")

        # deal with insertions to postcode

        # see if postcode already in database
        cur.execute("""SELECT id FROM postcode WHERE code = %s;""", [self.postcode])

        # if it does, remember the id; else, insert into postcode
        postcode_id: tuple[int] | None = cur.fetchone()

        if postcode_id is None:
            # insert into postcode table
            cur.execute(
                """ INSERT INTO postcode(code, road_name) 
                            VALUES (%s, %s);""",
                [self.postcode, self.road_name],
            )
            conn.commit()
            postcode_id: int = cur.lastrowid
        else:
            postcode_id: int = postcode_id[0]  # type: ignore

        cur.execute(
            """ INSERT INTO household(name, password, max_residents, postcode_id) 
                        VALUES (%s, %s, %s, %s)""",
            [
                self.name,
                str(self.password, encoding="utf8"),
                self.max_residents,
                postcode_id,
            ],
        )

        conn.commit()

        # update self id
        self.h_id = cur.lastrowid

    def delete(self, conn: MySQLConnection):
        """Deletes house from the database given there is only one person in the house"""

        cur: MySQLCursor = conn.cursor()

        # check how many people in the house
        cur.execute(
            """SELECT count(household_id) FROM user WHERE household_id = %s""",
            [self.h_id],
        )
        usr_count_row: tuple[int] = cur.fetchone()  # type: ignore

        if usr_count_row is None:
            # allow empty houses to be deleted for debugging
            usr_count: int = 0
        else:
            usr_count = usr_count_row[0]

        if usr_count > 1:
            raise HouseDeletionError(
                f"House has {usr_count} residents, and thus cannot be deleted"
            )

        # remove foreign key reference from remaining user
        cur.execute(
            """UPDATE user SET household_id = null WHERE household_id = %s""",
            [self.h_id],
        )

        # delete household
        cur.execute("""DELETE FROM household WHERE id = %s""", [self.h_id])

        # commit changes
        conn.commit()
