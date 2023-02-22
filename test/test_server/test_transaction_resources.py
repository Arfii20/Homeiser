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

    def test_patch(self):
        """Checks that we toggle paid and unpaid properly. Done by reading off a transaction and storing it,
        then sending the patch request, then reading off the same transaction. The 'before' and 'after'
        transactions are compared. Test passes if paid is different and every other field is the same"""

        # FIXME: Database updates with the patch command, but after request still provides the un-updated value for
        #  paid. Very confusing

        # create a cursor
        conn = mysql.connector.connect(
            host="localhost", user="root", password="HALR0b0t!12", database="x5db"
        )
        db = conn.cursor(buffered=True)
        conn.autocommit = True


        # store transaction 2
        before = trn.Transaction.build_from_id(transaction_id=2, cur=db)


        requests.patch(BASE + 'transaction/2')
        after = trn.Transaction.build_from_id(transaction_id=2, cur=db)

        with self.subTest("paid has changed"):
            self.assertNotEqual(before.paid, after.paid)

        with self.subTest("other fields unchanged"):
            self.assertEqual([v for v in before.__dict__][:-1],
                             [v for v in after.__dict__][:-1])
