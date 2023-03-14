import datetime
from unittest import TestCase

import mysql.connector

from transactions.transaction import Transaction
from transactions.ledger import Ledger, LedgerConstructionError


class TestLedger(TestCase):

    def setUp(self) -> None:
        """Make sure relevant rows are present in database"""

        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        db = conn.cursor()

        # remove any transactions under 428, 429, 430 which exist
        db.execute("DELETE FROM transaction WHERE id=428 OR id=429 OR id=430;")

        rows = [
            (428, 8, 10, 'a->b', datetime.date(2023, 3, 13), 0),
            (429, 9, 5, 'c->b', datetime.date(2023, 3, 13), 0),
            (430, 10, 5, 'a->c', datetime.date(2023, 3, 13), 0)
        ]

        # insert test rows
        for row in rows:
            db.execute("""INSERT INTO transaction VALUES (%s, %s, %s, %s, %s, %s) """, row)

        # commit changes
        conn.commit()


    def test_build_from_user_id(self):
        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        db = conn.cursor()

        with self.subTest("Successful construction"):
            self.l = Ledger.build_from_user_id(1, db)

        with self.subTest("User doesn't exist"):
            with self.assertRaises(LedgerConstructionError):
                Ledger.build_from_user_id(12312341231, db)

    def test_build_from_house_id(self):
        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        db = conn.cursor()

        # check that building from an id which doesn't exist fails
        with self.subTest("House ID doesn't exist"), self.assertRaises(
            LedgerConstructionError
        ):
            Ledger.build_from_house_id(-1, db)

        with self.subTest("Build house 2"):
            l = Ledger.build_from_house_id(3, db)

        expected = [
            Transaction.build_from_id(transaction_id=428, cur=db),
            Transaction.build_from_id(transaction_id=429, cur=db),
            Transaction.build_from_id(transaction_id=430, cur=db),
        ]

        self.assertEqual(l.transactions, expected)

    def test_users(self):
        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        db = conn.cursor()
        l = Ledger.build_from_house_id(3, db)

        exp = [(5, "Andrew Lees"), (6, "Bandicoot Crash"), (7, "Kez Carey")]

        u = l.users
        u.sort(key=lambda x: x[0])  # order ascending by id

        self.assertEqual(u, exp)

    def test_simplify(self):
        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        db = conn.cursor()
        Ledger.simplify(3, db)
