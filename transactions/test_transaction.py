import datetime
import json
from unittest import TestCase
from transaction import *


class TestTransaction(TestCase):
    def test_json(self):
        """Make sure json in correct format"""

        expected = json.dumps({
            "src": "Alice",
            "dest": "Bob",
            "amount": 10,
            "description": "test",
            "due_date": '2023-02-17T13:34:12.823836',
            "paid": "false"
        })

        transaction = Transaction(0, 0, 0, 10, datetime.datetime(2023, 2, 17, 13, 34, 12, 823836), False, "test", "Alice", "Bob")

        self.assertEqual(transaction.json, expected)