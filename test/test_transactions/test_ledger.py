from unittest import TestCase

import mysql.connector

from transactions.ledger import Ledger


class TestLedger(TestCase):
    def setUp(self):
        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="HALR0b0t!12", database="x5db"
        )
        db = conn.cursor()
        self.l = Ledger.build_from_id(1, db)

    def test_build_from_id(self):
        print(self.l)

    def test_json(self):
        print(self.l.json)
