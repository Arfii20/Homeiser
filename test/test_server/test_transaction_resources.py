from unittest import TestCase
import json
import mysql.connector
import requests

import transactions.transaction as trn

BASE = "http://127.0.0.1:5000/"


class TestTransactionResources(TestCase):
    def test_get(self):
        """Ensures get request returns transaction object in the correct format"""

        tests = ["Get an existing transaction", "Transaction doesn't exist"]
        params = ["transaction/1", "transaction/3"]
        expected = [
            (
                '{"transaction_id": 1, '
                '"src_id": 1, '
                '"dest_id": 2, '
                '"src": "Alice _", '
                '"dest": "Bob _", '
                '"amount": 10, '
                '"description": "test", '
                '"due_date": "2023-02-17", '
                '"paid": "false"}',
                200,
            ),
            (
                "Couldn't find transaction in the database; likely due to invalid transaction ID",
                404,
            ),
        ]

        for test, param, expect in zip(tests, params, expected):
            with self.subTest(test):
                got = requests.get(BASE + param)
                self.assertEqual((got.json(), got.status_code), expect)

    def test_post(self):

        # create a cursor
        conn = mysql.connector.connect(
            host="localhost", user="root", password="HALR0b0t!12", database="x5db"
        )
        db = conn.cursor()

        # make a test transaction
        exp = trn.Transaction.build_from_id(transaction_id=1, cur=db)

        # make transaction from dest -> src instead of src -> dest. Double amount owed
        # these are arbitrary changes to guarantee different transaction
        exp.src_id, exp.dest_id = exp.dest_id, exp.src_id
        exp.amount *= 2

        # add the newly modified transaction to the database
        r = requests.post('http://127.0.0.1:5000/transaction', json=exp.json)

        with self.subTest("add to db"):
            got = trn.Transaction.build_from_req(request=json.loads(r.json()))
            self.assertTrue(got.equal(exp))

        with self.subTest("attempt to add with incorrect json"):
                got = requests.post('http://127.0.0.1:5000/transaction', json='{"Should": "Fail"}')
                self.assertEqual(got.status_code, 400)
                self.assertEqual(got.json(), "Incorrect JSON Format for Transaction object")
