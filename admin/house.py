from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flask import Request
    from mysql.connector import MySQLConnection


class HouseConstructionError(Exception):
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
            r["postcode"] = r["postcode"].replace(' ', '').upper()
            r["road_name"] = r["road_name"].replace(' ', '').upper()

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
        ...

    def insert_to_db(self, conn: MySQLConnection):
        """Inserts the house into the database"""

        cur = conn.cursor()

        # deal with insertions to postcode

        # see if postcode already in database
        cur.execute("""SELECT id FROM postcode WHERE code = %s""", [self.postcode])

    def delete(self, conn: MySQLConnection):
        ...
