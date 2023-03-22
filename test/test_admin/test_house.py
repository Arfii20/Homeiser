from unittest import TestCase
from admin.house import House
import mysql.connector


class TestHouse(TestCase):
    def setUp(self) -> None:
        self.house = House(0, "test", b"", 10, "SEYMOUR ROAD", "KT8PF")

    def test_build_from_request(self):
        ...

    def test_build_from_id(self):
        ...

    def test_insert_to_db(self):
        # connect to db
        conn = mysql.connector.connect(
            host="localhost", user="root", password="I_love_stew!12", database="x5db"
        )

        db = conn.cursor()

        self.house.insert_to_db(conn)

    def test_delete(self):
        ...

    def test_json(self):
        print(self.house.json)
