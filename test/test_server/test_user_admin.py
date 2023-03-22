import datetime
import json
from unittest import TestCase

import requests
import mysql.connector

from admin.user import User
from admin.house import House

target = "http://127.0.0.1:5000/"


class TestUserResource(TestCase):
    def setUp(self):
        # connect to db
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        self.user = User(
            None,
            "test",
            "user",
            "test@user.com",
            "test",
            datetime.date(1, 1, 1),
            None,
            None,
        )

    def test_get(self):
        r = requests.get(target + "user/alice@alice.com")
        exp = (
            '{"user_id": 1, '
            '"first_name": "Alice", '
            '"surname": "_", '
            '"email": "alice@alice.com", '
            '"password": "", '
            '"dob": "0001-02-02", '
            '"household_id": 1, '
            '"colour": null}'
        )


        with self.subTest("exists"):
            self.assertEqual(exp, r.json())

        r = requests.get(target + "user/dsafaswedf.com")
        with self.subTest("email doesn't exist"):
            print(r.json())
            self.assertEqual(r.status_code, 404)

    def test_post(self):
        for test, exp in zip(["posts", "fails as email already exists"], [201, 500]):
            with self.subTest(test):
                r = requests.post(
                    target + "/user",
                    headers={"Content-Type": "application/json"},
                    json=self.user.json,
                )
                print(r.status_code, "\n", r.json())
                self.assertEqual(r.status_code, exp)

        self.conn.commit()

        cur = self.conn.cursor(buffered=True)

        try:
            cur.execute("""DELETE FROM user ORDER BY id DESC LIMIT 1""")
        except:
            ...

        self.conn.commit()

    def test_patch(self):
        # insert new user
        requests.post(
            target + "/user",
            headers={"Content-Type": "application/json"},
            json=self.user.json,
        )

        # make user join household
        requests.patch(target + "/user/1/test@user.com/1")

        # check that user has joined household 1
        cur = self.conn.cursor(buffered=True)
        cur.execute(
            """SELECT household_id FROM user WHERE email = %s""", [self.user.email]
        )

        with self.subTest("Joined household"):
            self.assertEqual((1,), cur.fetchone())

        # leave household
        requests.patch(target + "/user/1/test@user.com/0")

        cur2 = self.conn.cursor(buffered=True)

        cur2.execute(
            """SELECT household_id FROM user WHERE email = %s""", [self.user.email]
        )
        with self.subTest("Joined household"):
            self.assertEqual(None, cur.fetchone())

        # cleanup
        cur2.execute(f"""DELETE FROM user WHERE id = {cur.lastrowid}""")
        self.conn.commit()

    def test_delete(self):
        # insert user
        requests.post(
            target + "/user",
            headers={"Content-Type": "application/json"},
            json=self.user.json,
        )

        # delete user
        requests.delete(target + f"/user/{self.user.email}")

        # check delete has happened
        cur = self.conn.cursor()
        cur.execute(
            """SELECT household_id FROM user WHERE email = %s""", [self.user.email]
        )

        self.assertEqual(cur.fetchone(), (None,))


class TestHouseResource(TestCase):

    def setUp(self):
        # connect to db
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        self.house = House(0, "test", "test_password", 10, "SEYMOUR ROAD", "KT8PF")

    def test_get(self):
        r = requests.get(target + "/house/1")
        self.assertEqual(
            json.loads(r.json()),
            {
                "h_id": 1,
                "name": "Flat 97",
                "password": "",
                "max_residents": 6,
                "road_name": "DENMARK ROAD",
                "postcode": "M156GQ",
            },
        )

    def test_post(self):

        # create house
        requests.post(
            target + "/house",
            headers={"Content-Type": "application/json"},
            json=self.house.json,
        )

        # check house is there
        cur = self.conn.cursor()
        cur.execute("""SELECT id FROM household ORDER BY id DESC LIMIT 1""")
        h_id = cur.fetchone()[0]

        self.assertGreater(h_id, 3, msg="New household inserted")



    def test_delete(self):
        # create house
        r = requests.post(
            target + "/house",
            headers={"Content-Type": "application/json"},
            json=self.house.json,
        )


        # delete house
        h_id =  json.loads(r.json())['h_id']

        requests.delete(target + f'/house/{h_id}')

        # make sure it no longer exists
        cur = self.conn.cursor()
        cur.execute("""SELECT id FROM household ORDER BY id DESC LIMIT 1""")
        max_id = cur.fetchone()[0]

        self.assertLess(max_id, h_id)
