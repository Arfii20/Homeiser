from unittest import TestCase
from admin.house import House


class TestHouse(TestCase):
    def setUp(self) -> None:
        self.house = House(0, 'test', b'', 10, 'Seymour', 'KT8 0PF')

    def test_build_from_request(self):
        ...

    def test_build_from_id(self):
        ...

    def test_insert_to_db(self):
        ...

    def test_delete(self):
        ...

    def test_json(self):
        print(self.house.json)
