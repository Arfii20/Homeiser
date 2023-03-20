from unittest import TestCase

import requests

target = "http://127.0.0.1:5000/"


class TestUserResource(TestCase):
    def test_get(self):
        r = requests.get(target + "user/alice@alice.com")
        exp = (
            '{"user_id": 1, '
            '"first_name": "Alice", '
            '"surname": "_", '
            '"email": "alice@alice.com", '
            '"password": "alice", '
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
