from unittest import TestCase

import mysql.connector

from transactions.ledger import Ledger, LedgerConstructionError


class TestLedger(TestCase):
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

    def test_json(self):
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )
        db = conn.cursor()

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
