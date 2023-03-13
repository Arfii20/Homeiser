from __future__ import annotations

import datetime
import json
from dataclasses import dataclass

import requests
from mysql.connector import cursor


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
    house_id: int

    @property
    def json(self) -> str:
        """Returns a JSON representation of transaction object of the format

        {   "transaction_id": <int:transaction id>
            "src_id": <int: src id>
            "dest_id": <int: dest id>
            "src": <str:src full name>,
            "dest": <str:dest full name>,
            "amount": <int: amount>,
            "description": <str: description>
            "due_date": <str:date string in format yyyy-mm-dd>
            "paid": <int: boolean>
            "house_id": <int:>
        }
        """
        try:
            dump = json.dumps(
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
                    "household_id": self.house_id,
                }
            )
            return dump

        except json.decoder.JSONDecodeError as je:
            raise ValueError("Failed to convert transaction to JSON", je)

    @staticmethod
    def build_from_id(*, transaction_id: int, cur: cursor.MySQLCursor) -> Transaction:
        """Builds a transaction from an id in the db and a cursor to said database"""

        cur.execute(
            "SELECT transaction.id, u1.id, u2.id,  CONCAT_WS(' ', u1.first_name, u1.surname), "
            "CONCAT_WS(' ', u2.first_name, u2.surname), amount, description, due_date, paid, u1.household_id "
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

        # convert paid in {0, 1} -> True/False
        args[-2] = bool(args[-2])

        return Transaction(*args)

    @staticmethod
    def build_from_req(*, request: requests.Response | dict) -> Transaction:
        """Build a transaction object from an HTTP request"""

        # load json representation of Transaction into a dict if it is not already a dict
        if type(request) != dict:
            r = json.loads(request.json())  # type: ignore
        else:
            r = request

        try:
            # clean data so can unpack values of dict straight into Transaction

            # convert date from str to datetime.date object if we haven't been given a datetime.date object
            if type(r["due_date"]) is not datetime.date:
                r["due_date"] = datetime.date(
                    *[int(d) for d in r["due_date"][:10].split("-")]
                )

            # Convert paid from string to bool object
            r["paid"] = True if r["paid"] == "true" else False

            # build transaction object
            transaction = Transaction(*r.values())

        # if we get a key error then JSON wasn't in correct format
        except KeyError as ke:
            raise TransactionConstructionError(ke)

        return transaction

    def equal(self, other: Transaction) -> bool:
        """compares equality based on value of every field except t_id"""
        return [v for v in self.__dict__.values()][1:] == [
            v for v in other.__dict__.values()
        ][1:]


@dataclass
class CalendarEvent:
    """Represents one event in the calendar

    JSON Format:

        {
        'event_id': list[int],
        'title_of_event': list[str],
        "starting_time": list[str], where str is in the form "yyyy-mm-dd HH:MM:SS"
        "ending_time": ["yyyy-mm-dd HH:MM:SS"],
        'additional_notes': list[str],
        'location_of_event': list[str],
        "household_id": list[int],
        "tagged_users": list[int],
        'added_by': list[int]
        }

    """

    event_id: int
    title: str
    start: datetime.datetime
    end: datetime.datetime
    notes: str
    location: str
    house: int
    tags: list[int]
    added_by: int

    @staticmethod
    def from_transaction(transaction: Transaction) -> CalendarEvent:
        """Builds a calendar object from a transaction. Uses the Transaction object's ID.
        This ID is NOT a calendar_event ID. It cannot be involved in queries regarding calendar_events
        """

        return CalendarEvent(
            event_id=transaction.t_id,
            title=f"{transaction.src_name} -> {transaction.dest_name}",
            start=datetime.datetime.combine(transaction.due, datetime.time(0, 0, 0)),
            end=datetime.datetime.combine(transaction.due, datetime.time(23, 59, 59)),
            notes=transaction.description,
            location="",
            house=transaction.house_id,
            tags=[transaction.dest_id],
            added_by=transaction.src_id,
        )

    @property
    def json(self) -> str:
        """
        Dumps CalendarEvent to JSON. Format is defined in implementation of CalendarEvent
        and used here
        """
        as_dict = {
            "event_id": [self.event_id],
            "title_of_event": [self.title],
            "starting_time": [self.datetime_to_propiatery(self.start)],
            "ending_time": [self.datetime_to_propiatery(self.end)],
            "additional_notes": [self.notes],
            "location_of_event": [self.location],
            "household_id": [self.house],
            "tagged_users": self.tags,
            "added_by": [self.added_by],
        }

        return json.dumps(as_dict)

    @staticmethod
    def datetime_to_propiatery(dt: datetime.datetime) -> str:
        """JSON for Calendar object calls for datetimes to be formatted in YYYY-MM-DD HH:MM:SS.
        Given a datetime object this method will return the date in propriatery format
        """

        return f"{dt.isoformat()[:10]} {dt.hour}:{dt.minute}:{dt.second}"
