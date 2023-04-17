import datetime
from unittest import TestCase

import mysql.connector

from admin.user import User, UserError
from transactions.transaction import Transaction
import requests


def setUpModule():
    """Check that first 7 rows of user db are as expected"""

    # connect to db
    conn = mysql.connector.connect(
        host="localhost", user="root", password="I_love_stew!12", database="x5db"
    )

    db = conn.cursor(buffered=True)

    db.execute("""SELECT * FROM user;""")

    # make sure that first 7 rows in db are as expected
    expected_user_table = [
        (1, "Alice", "_", "alice", "alice@alice.com", datetime.date(1, 2, 2), 1, None),
        (2, "Bob", "_", "bob", "bob@bob.com", None, 1, None),
        (3, "Test", "Ledger", "l", "l@l.com", datetime.date(1, 2, 2), 2, None),
        (4, "Test2", "Ledger", "l", "l@2.com", datetime.date(1, 1, 1), 2, None),
        (5, "Andrew", "Lees", "alees", "a@a.com", datetime.date(2023, 3, 13), 3, None),
        (6, "Bandicoot", "Crash", "bc", "b@c.com", datetime.date(2023, 3, 13), 3, None),
        (7, "Kez", "Carey", "kc", "k@c.com", datetime.date(2023, 3, 13), 3, None),
    ]

    received = db.fetchall()

    for exp, got in zip(expected_user_table, received):
        if exp != got:
            # if there is a discrepancy delete row and insert the correct row
            db.execute(
                "UPDATE user "
                "SET "
                "first_name = %s, "
                "surname = %s, "
                "password = %s, "
                "email = %s, "
                "date_of_birth = %s, "
                "household_id = %s, "
                "color = %s "
                "WHERE id=%s",
                [*exp[1:], exp[0]],
            )

    # add user a and user b for testing delete user, and transactions from a->b and b->a

    usrs = [
        User(200, "a", "", "a@testdel.com", b"a", None, 1, None),
        User(201, "b", "", "b@testdel.com", b"b", None, 1, None),
    ]

    db.execute("""SELECT id FROM user WHERE id = %s OR id = %s""", [200, 201])
    ids = db.fetchall()

    if not ids:
        for usr in usrs:
            usr.insert_to_database(db, conn)

    conn.commit()

    # transaction a -> b
    t1 = Transaction(0, 200, 201, "a", "b", 5, "", datetime.date(3000, 1, 1), False, 1)

    # transaction b -> a
    t2 = Transaction(0, 201, 200, "b", "a", 10, "", datetime.date(3000, 1, 1), False, 1)

    t1.insert_transaction(db, conn)
    t2.insert_transaction(db, conn)


class TestUser(TestCase):
    def test_insert_to_database(self):
        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        db = conn.cursor()

        john = User(
            0,
            "John",
            "Heereboys",
            "j@heere.com",
            b"test",
            datetime.date(1, 1, 1),
            None,
            None,
        )
        john.insert_to_database(db, conn)

        del db
        cur2 = conn.cursor()

        # ensure that insert worked
        cur2.execute("""SELECT * FROM user WHERE email = %s""", ["j@heere.com"])

        got = cur2.fetchall()[0]

        with self.subTest("Insert"):
            self.assertEqual(
                got[1:],
                (
                    "John",
                    "Heereboys",
                    "test",
                    "j@heere.com",
                    datetime.date(1, 1, 1),
                    None,
                    None,
                ),
            )

        # cleanup
        cur2.execute("""DELETE FROM user WHERE id = %s""", [got[0]])
        conn.commit()

        # try to insert where an email adress already exists
        fail = User(
            0,
            "John",
            "Heereboys",
            "l@l.com",
            b"test",
            datetime.date(1, 1, 1),
            None,
            None,
        )

        with self.subTest("email exists"), self.assertRaises(UserError):
            fail.insert_to_database(cur2, conn)

    def test_join_household(self):
        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        db = conn.cursor()

        # create a user with no household and insert into db
        john = User(
            0,
            "John",
            "Heereboys",
            "j@heere.com",
            b"test",
            datetime.date(1, 1, 1),
            None,
            None,
        )
        john.insert_to_database(db, conn)

        john.join_household(2, db, conn)

        del db
        cur = conn.cursor()
        cur.execute("""SELECT household_id FROM user WHERE email = 'j@heere.com'""")

        self.assertEqual(cur.fetchone()[0], 2)

        cur.execute("""DELETE FROM user WHERE email = 'j@heere.com'""")
        conn.commit()

    def test_leave_household(self):
        """Three subtests:
        1: fail - person who is not part of a house tries to leave household
        2: fail - person who is involved in transactions tries to leave household
        3: success - person with no transactions leaves the household
        """

        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        cur = conn.cursor()

        person1 = User(
            0,
            "No",
            "Transactions",
            "j@heere.com",
            b"test",
            datetime.date(1, 1, 1),
            None,
            None,
        )

        person2 = User(
            5,
            "Andrew",
            "Lees",
            "a@a.com",
            b"alees",
            datetime.date(2023, 3, 13),
            3,
            None,
        )

        person1.insert_to_database(cur, conn)

        with self.subTest("User not in household"), self.assertRaises(UserError):
            person1.leave_household(cur, conn)

        with self.subTest("User has open transactions"), self.assertRaises(UserError):
            person2.leave_household(cur, conn)

        # make person1 join a house, and then check they leave successfully
        person1.join_household(3, cur, conn)
        cur2 = conn.cursor()
        person1.leave_household(cur2, conn)

        cur2.execute("SELECT household_id FROM user WHERE email='j@heere.com'")
        h_id = cur2.fetchone()[0]

        with self.subTest("Successful leave"):
            self.assertIsNone(h_id)

        # cleanup
        cur2.execute("""DELETE FROM user WHERE email = 'j@heere.com'""")
        conn.commit()

    def test_delete(self):
        """In setup, two users, a and b created.
        There exists a transaction a->b, and b-> a. delete a. delete b."""

        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        db = conn.cursor()

        usrs = [
            User(200, "a", "", "a@testdel.com", b"a", None, 1, None),
            User(201, "b", "", "b@testdel.com", b"b", None, 1, None),
        ]

        for usr in usrs:
            usr.delete(db, conn)

        # make sure users no longer exist
        cur = conn.cursor()
        cur.execute(
            """SELECT id FROM transaction WHERE id = %s OR id = %s""", [200, 201]
        )
        results = cur.fetchall()
        self.assertFalse(results)

    def test_build_from_email(self):
        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        db = conn.cursor()

        exp_user = User(
            1,
            "Alice",
            "_",
            "alice@alice.com",
            b"alice",
            datetime.date(1, 2, 2),
            1,
            None,
        )
        got_usr = User.build_from_email("alice@alice.com", db)
        with self.subTest("User built"):
            self.assertEqual(exp_user.json, got_usr.json)

        with self.subTest("No user with email"), self.assertRaises(UserError):
            User.build_from_email("asfas", db)

    def test_build_from_req(self):
        """Try to build User object from request"""
        target = "http://127.0.0.1:5000/"

        r = requests.get(target + "user/alice@alice.com")
        alice = User.build_from_req(request=r)

        print(alice.json)
