from __future__ import annotations

from dataclasses import dataclass
import datetime
import json
from mysql.connector import cursor
import requests


class TransactionConstructionError(Exception):
    """Triggered when a transaction failed to build from the database"""


@dataclass
class Transaction:
    """Specifies a singular transaction"""

    t_id: int
    src_id: int
    dest_id: int
    src_name: str
    dest_name: str
    amount: int
    description: str
    due: datetime.date
    paid: bool

    @property
    def json(self) -> str:
        """Returns a JSON representation of transaction object of the format

        {   "transaction_id": <int:transaction id>
            "src_id": <int: src id>
            "dest_id": <int: dest id>
            "src": <str:src full name>,
            "dest": <str:dest full name>,
            "amount": <int:amount>,
            "description": <str:description>
            "due_date": <str:date string in format yyyy-mm-dd>
            "paid": <str:boolean>
        }
        """

        return json.dumps(
            {
                "transaction_id": self.t_id,
                "src_id": self.src_id,
                "dest_id": self.dest_id,
                "src": self.src_name,
                "dest": self.dest_name,
                "amount": self.amount,
                "description": self.description,
                "due_date": self.due.isoformat(),
                "paid": "true" if self.paid else "false",
            }
        )

    @staticmethod
    def build_from_id(*, transaction_id: int, cur: cursor.MySQLCursor) -> Transaction:
        """Builds a transaction from an id in the db and a cursor to said database"""

        cur.execute(
            "SELECT transaction.id, u1.id, u2.id,  CONCAT_WS(' ', u1.first_name, u1.surname), "
            "CONCAT_WS(' ', u2.first_name, u2.surname), amount, description, due_date, paid "
            "FROM transaction, pairs, user u1, user u2 "
            "WHERE transaction.id = %s AND pairs.id = transaction.pair_id"
            " AND u1.id = pairs.src AND u2.id = pairs.dest",
            [transaction_id],
        )

        # only one row will match an ID
        # throw an exception if no transaction returned
        # complain if None is returned

        if (row := cur.fetchone()) is None:
            raise TransactionConstructionError(
                "Couldn't find transaction in the database; "
                "likely due to invalid transaction ID"
            )
        else:
            args: list = [element for element in row]

        # args is in the form
        # [transaction_id: int, src_id: int, dest_id: int, amount: int, due_date: str, paid: int,
        # description: str, src_name: str, dest_name: str]

        # need to convert paid from int -> bool
        # do in place so can pass tuple directly into Transaction() instantiation

        args[-1] = bool(args[-1])

        return Transaction(*args)

    @staticmethod
    def build_from_req(
        request: requests.Response, cur: cursor.MySQLCursor
    ) -> Transaction:
        """Build a transaction object from an HTTP request"""

        r = json.loads(request.json())

        # get pair id
        cur.execute(
            "SELECT id FROM pairs WHERE src = %s AND dest = %s",
            [r["src_id"], r["dest_id"]],
        )
        pair_id = cur.fetchone()

        if pair_id is None:
            # add pair to pairs table if the pair doesn't already exist
            cur.execute(
                "INSERT INTO pairs(src, dest) VALUES (%s, %s)",
                [r["src_id"], r["dest_id"]],
            )

            # get id from pair entry that was just generated
            cur.execute(
                "SELECT id FROM pairs WHERE src = %s AND dest = %s",
                [r["src_id"], r["dest_id"]],
            )
            pair_id = cur.fetchone()

        # clean data so can unpack values of dict straight into Transaction init

        # convert date from str to datetime.date object
        r["due_date"] = datetime.date(*[int(d) for d in r["due_date"].split("-")])

        # Convert bool string to bool object
        r["paid"] = True if r["paid"] == "true" else False

        # build transaction object
        return Transaction(*r.values())
