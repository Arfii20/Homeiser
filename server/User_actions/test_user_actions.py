import requests
import unittest
import datetime

BASE = "http://127.0.0.1:5000/"

class TestRegisterUser(unittest.TestCase):
    def test_user_post_bad(self):
        response = requests.post(BASE + "register_user/1", {"id": 1, "firstname": "Bob", "surname": "Smith", "password":"hello123", "email":"hello@gmail.com", "date_of_birth": datetime.datetime(2001,12,12), "color":1})
        self.assertEqual(response.json(), {"Error":"user email must be unique"})

    def test_user_post_good(self):
        response = requests.post(BASE + "register_user/1", {"id": 397, "firstname": "Bob", "surname": "Smith", "password1":"hello123", "password2":"hello123", "email":"hello397@gmail.com", "date_of_birth": datetime.datetime(2001,12,12), "color":1})
        self.assertEqual(response.json(), {"Message":"user created successfully"})

class TestLoginUser(unittest.TestCase):
    def test_user_login_bad(self):
        response = requests.post(BASE + "login_user/1", {"email": "hello@gmail.com", "password":"IncorrectPassword"}
        self.asserEqual(response.json(), {"Error":"incorrect email or password entered"})

    def test_user_login_good(self):
        response = requests.post(BASE + "login_user/1",{"email": "hello@gmail.com", "password": "hello123"}
        self.asserEqual(response.json(), {"Message": "Logged in successfully"})

class TestRegisterHouse(unittest.TestCase):
    def test_house_post_bad(self):
        response = requests.post(BASE + "register_house/1", {"id": 1, "name": "BobHouse" ,"password1": "House123","password2":"House123", "max_residents":4, "postcode_id":3, "postcode":"M17 5GH", "road_name": "15 Oxford Road"}
        self.assertEqual(response.json(), {"Error": "house must be unique"})

    def test_house_post_good(self):
        response = requests.post(BASE + "register_house/1" ,{"id": 947, "name": "JennyHouse", "password1": "jenny123", "password2": "jenny123", "max_residents": 4, "postcode_id": 943, "postcode": "M17 5GH", "road_name": "15 Oxford Road"}
        self.assertEqual(response.json(), {"Message": "House created successfully"})

class TestLoginHouse(unittest.TestCase):
    def test_house_login_bad(self):
        response = requests.post(BASE + "login_house/1",{"name": "BobHouse", "password": "IncorrectPassword"}
        self.asserEqual(response.json(), {"Error": "incorrect name or password entered"})

    def test_house_login_good(self):
        response = requests.post(BASE + "login_house/1", {"name": "BobHouse", "password": "House123"}
        self.asserEqual(response.json(), {"Message": "Logged in successfully"})


if __name__ == '__main__':
    unittest.main()