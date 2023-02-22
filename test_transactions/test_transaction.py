from transactions.transaction import *
from unittest import TestCase

import mysql.connector


class TestTransaction(TestCase):
    def test_json(self):
        """Make sure json in correct format"""

        expected = json.dumps(
            {
                "src": "Alice",
                "dest": "Bob",
                "amount": 10,
                "description": "test",
                "due_date": "2023-02-17",
                "paid": "false",
            }
        )

        transaction = Transaction(
            0, 0, 0, 10, datetime.date(2023, 2, 17), False, "test", "Alice", "Bob"
        )

        self.assertEqual(transaction.json, expected)

    def test_build_from_id(self):
        """Checks that we build a transaction object properly when we ask for one (given an id)
        Also checks that a TransactionConstructionError is thrown when the database does not exist
        """

        expect = Transaction(
            1, 1, 2, 10, datetime.date(2023, 2, 17), False, "test", "Bob _", "Alice _"
        )

        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="HALR0b0t!12", database="x5db"
        )
        db = conn.cursor()

        got = Transaction.build_from_id(transaction_id=1, cur=db)

        with self.subTest("Fetch from id=1"):
            self.assertEqual(expect, got, "Transaction objects")

        with self.subTest("Fetch form id=-1"):
            with self.assertRaises(TransactionConstructionError):
                Transaction.build_from_id(transaction_id=-1, cur=db)
