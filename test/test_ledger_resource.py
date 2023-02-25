import json
from unittest import TestCase

import requests


class TestLedgerResource(TestCase):
    def test_get(self):
        """Checks we get a response of transactions from user called Test Ledger"""

        r = requests.get("http://127.0.0.1:5000/ledger/3")

        exp_json = [
            '{"transaction_id": 4, "src_id": 3, "dest_id": 4, "src": "Test Ledger",'
            ' "dest": "Test2 Ledger", "amount": 20, "description": "test", '
            '"due_date": "2023-02-17", "paid": "false", "household_id": 1}'
        ]

        with self.subTest("Get user transactions where user exists"):
            self.assertEqual(r.status_code, 200)
            self.assertEqual(json.dumps(exp_json), r.json())

        r = requests.get("http://127.0.0.1:5000/ledger/34523452354")

        with self.subTest("Expect 404 where user doesn't exist"):
            self.assertEqual(r.status_code, 404)
