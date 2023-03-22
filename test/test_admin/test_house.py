import json
from unittest import TestCase
from admin.house import House, HouseConstructionError, HouseDeletionError, HouseInsertionError
import mysql.connector


class TestHouse(TestCase):
    def setUp(self) -> None:
        self.house = House(0, "test", b"", 10, "SEYMOUR ROAD", "KT8PF")

        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        self.h3 = House(3, "simple", b"simple", 3, "M156GQ", "DENMARK ROAD")
        try:
            self.h3.insert_to_db(self.conn)
        except HouseInsertionError:
            ...

    def test_build_from_request(self):
        ...

    def test_build_from_id(self):

        with self.subTest("Successful build"):
            self.assertEqual(
                json.loads(House.build_from_id(3, self.conn).json),
                {
                    "h_id": 3,
                    "name": "simple",
                    "password": "",
                    "max_residents": 3,
                    "road_name": "DENMARK ROAD",
                    "postcode": "M156GQ",
                },
            )

        with self.subTest("id doesnt exist"), self.assertRaises(HouseConstructionError):
            House.build_from_id(123123123123, self.conn)

    def test_insert_to_db(self):
        # connect to db

        conn = self.conn

        db = conn.cursor()
        self.house.insert_to_db(conn)

        db.execute(
            """SELECT household.id, name, password, max_residents, road_name, code FROM household
        JOIN postcode p on p.id = household.postcode_id
        WHERE household.id = %s""",
            [self.house.h_id],
        )

        row = db.fetchone()

        exp = self.house.__dict__
        exp["password"] = str(exp["password"], encoding="utf8")

        self.assertEqual(
            self.house.__dict__, {k: v for k, v in zip(self.house.__dict__.keys(), row)}
        )

        # cleanup
        db.execute("""DELETE FROM household WHERE id = %s""", [self.house.h_id])
        conn.commit()

    def test_delete(self):
        # insert house into db
        self.house.insert_to_db(self.conn)

        last_row = self.house.h_id
        self.house.delete(self.conn)

        # verify that the house no longer exists
        cur = self.conn.cursor()

        cur.execute(f"""SELECT count(*) FROM household WHERE id = {last_row}""")

        with self.subTest("successful delete"):
            self.assertEqual(cur.fetchone(), (0,))

        # try to delete a house with users that exist
        with self.subTest("Fail as there are >1 users in the house"), self.assertRaises(
                HouseDeletionError
        ):
            self.h3.delete(self.conn)

    def test_json(self):
        print(self.house.json)
