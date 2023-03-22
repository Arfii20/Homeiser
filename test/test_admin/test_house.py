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

        db.execute("""SELECT household.id, name, password, max_residents, road_name, code FROM household
        JOIN postcode p on p.id = household.postcode_id
        WHERE household.id = %s""", [self.house.h_id])

        row = db.fetchone()

        exp = self.house.__dict__
        exp["password"] = str(exp["password"], encoding='utf8')

        self.assertEqual(self.house.__dict__, {k: v for k, v in zip(self.house.__dict__.keys(), row)})

        # cleanup
        db.execute("""DELETE FROM household WHERE id = %s""", [self.house.h_id])
        conn.commit()

    def test_delete(self):
        ...

    def test_json(self):
        print(self.house.json)
