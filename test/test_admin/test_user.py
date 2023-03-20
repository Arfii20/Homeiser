import datetime
from unittest import TestCase
import mysql.connector

def setUpModule():
    """Check that first 7 rows of user db are as expected"""

    # connect to db
    conn = mysql.connector.connect(
        host="localhost", user="root", password="I_love_stew!12", database="x5db"
    )

    db = conn.cursor()

    db.execute("""SELECT * FROM user;""")

    # make sure that first 7 rows in db are as expected
    expected_user_table = [
        (1, "Alice", "_", 'alice', 'alice@alice.com', None, 1, None),
        (2, "Bob", "_", 'bob', 'bob@bob.com', None, 1, None),
        (3, "Test", "Ledger", 'l', 'l@l.com', datetime.date(1, 2, 2), 2, None),
        (4, "Test2", "Ledger", 'l', 'l@l.com', datetime.date(1, 1, 1), 2, None),
        (5, "Andrew", "Lees", 'alees', 'a@a.com', datetime.date(2023, 3, 13), 3, None),
        (6, "Bandicoot", "Crash", 'bc', 'b@c.com', datetime.date(2023, 3, 13), 3, None),
        (7, "Kez", "Carey", 'kc', 'k@c.com', datetime.date(2023, 3, 13), 3, None),
    ]


    received = db.fetchall()

    for exp, got in zip(expected_user_table, received):
        if exp != got:
            db.execute("DELETE ")


class TestUser(TestCase):

    def setUp(self) -> None:
        """insert rows needed for tests"""

        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        db = conn.cursor()



    def test_insert_to_database(self): ...

    def test_join_household(self): ...

    def test_leave_household(self): ...

    def test_delete(self): ...

    def test_build_from_email(self): ...

    def test_build_from_id(self): ...

    def test_json(self): ...
