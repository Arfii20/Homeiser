from typing import Any
from unittest import TestCase

import mysql.connector

from transactions.transaction import *


class MockPost:
    """Mocks post request"""

    def __init__(self, mock_json):
        self.mock_json = mock_json

    def json(self) -> Any:
        return self.mock_json


class TestTransaction(TestCase):
    def test_json(self):
        """Make sure json in correct format"""

        expected = json.dumps(
            {
                "transaction_id": 0,
                "src_id": 0,
                "dest_id": 0,
                "src": "Alice",
                "dest": "Bob",
                "amount": 10,
                "description": "test",
                "due_date": "2023-02-17",
                "paid": "false",
                "household_id": 1,
            }
        )

        transaction = Transaction(
            0, 0, 0, "Alice", "Bob", 10, "test", datetime.date(2023, 2, 17), False, 1
        )

        self.assertEqual(transaction.json, expected)

    def test_build_from_id(self):
        """Checks that we build a transaction object properly when we ask for one (given an id)
        Also checks that a TransactionConstructionError is thrown when the database does not exist
        """

        expect = Transaction(
            1,
            1,
            2,
            "Alice _",
            "Bob _",
            10,
            "test",
            datetime.date(2023, 2, 17),
            False,
            1,
        )

        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )
        db = conn.cursor()

        got = Transaction.build_from_id(transaction_id=1, cur=db)

        with self.subTest("Fetch from id=1"):
            self.assertEqual(expect, got, "Transaction objects")

        with self.subTest("Fetch form id=3"):
            with self.assertRaises(TransactionConstructionError):
                Transaction.build_from_id(transaction_id=-1, cur=db)

    def test_build_from_req(self):
        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )
        db = conn.cursor()

        # Create test transaction from database
        expected = Transaction.build_from_id(transaction_id=1, cur=db)

        # dump expected to json and use json to build a 'got' transaction
        got = Transaction.build_from_req(request=MockPost(expected.json))  # type: ignore

        with self.subTest("construct"):
            self.assertEqual(expected, got)

        with self.subTest("wrong format"):
            with self.assertRaises(TransactionConstructionError):
                Transaction.build_from_req(request={"test": "fails"})


class TestCalendarEvent(TestCase):
    def test_json(self):
        # set up expected JSON
        start = datetime.datetime(2023, 2, 23, 19, 51, 57, 441926)
        end = datetime.datetime(2023, 2, 23, 20, 2, 47, 797909)

        exp = json.dumps(
            {
                "event_id": [1],
                "title_of_event": ["Test"],
                "starting_time": [CalendarEvent.datetime_to_propiatery(start)],
                "ending_time": [CalendarEvent.datetime_to_propiatery(end)],
                "additional_notes": ["notes"],
                "location_of_event": ["location"],
                "household_id": [1],
                "tagged_users": [1, 2, 3],
                "added_by": [4],
            }
        )

        ce = CalendarEvent(1, "Test", start, end, "notes", "location", 1, [1, 2, 3], 4)

        self.assertEqual(exp, ce.json)

    def test_from_transaction(self):
        ...
