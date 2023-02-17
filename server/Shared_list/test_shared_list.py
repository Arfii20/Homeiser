import unittest
import requests
from random import randint

# from shared_list import SharedList, ListDetails

BASE = "http://127.0.0.1:5000/"


# class TestSharedList(unittest.TestCase):
# def test_post(self):
#     returned = shared_list.

class TestSharedList(unittest.TestCase):

    def test_shared_list_name_post_bad(self):
        response = requests.post(BASE + "shared_list/1", {"name": "Gr2s"})
        self.assertEqual(response.json(), {'Error': 'List Name Must Be Unique'})

    def test_shared_list_id_post_bad(self):
        file = open("words.txt")
        words = file.readlines()
        file_length = len(words) - 1
        while True:
            word = words[randint(0, file_length)]
            response = requests.post(BASE + "shared_list/1", {'id': 1,
                                                              "name": word[0:len(word) - 2]})

            if response.json() != {'Error': 'List Name Must Be Unique'}:
                break
        file.close()

        response = requests.post(BASE + "shared_list/1", {'id': 1, "name": word[0:len(word) - 2]})
        self.assertEqual(response.json(), {'Error': 'ID Must Be Unique'})

    def test_shared_list_post_good(self):
        file = open("words.txt")
        words = file.readlines()
        file_length = len(words) - 1
        while True:
            word = words[randint(0, file_length)]
            number = randint(0, 5000)
            if len(word) > 4:
                response = requests.post(BASE + "shared_list/1", {'id': number,
                                                                  "name": word[0:len(word) - 2]})
                if response.json() == {"Response": "List Created"}:
                    break
        file.close()
        requests.delete(f"{BASE}list_details/{number}")
        response = requests.post(BASE + "shared_list/1", {'id': number,
                                                          "name": word[0:len(word) - 2]})
        self.assertEqual(response.json(), {"Response": "List Created"})

    def test_shared_list_get(self):
        response = requests.get(BASE + "shared_list/1")
        valid = True
        print(response.json().keys())
        for i in response.json().keys():
            if i not in ['id', 'name', 'household_id']:
                valid = False
        self.assertTrue(valid)

    def test_shared_list_delete(self):
        response2 = requests.delete(BASE + "list_details/97")
        print(response2.json())


# response3 = requests.patch(BASE + "list_details/54", {"new_name": "Yameen"})
# print(response3.json())
#
# # List Items
# response4 = requests.post(BASE + "list_events/1", {"task_name": "Garbaage",
#                                                    "description_of_task": "Take the garbage outside "
#                                                                           "before evening please",
#                                                    "added_user_id": 1})
# print(response4.json())
#
# response5 = requests.get(BASE + "list_events/1")
# print(response5.json())

# response6 = requests.delete(BASE + "list_event_details/2")
# print(response6.json())

# response7 = requests.patch(BASE + "list_event_details/3", {"user_id": 1})
# print(response7.json())
# response8 = requests.patch(BASE + "list_event_details/3", {"user_id": 1})
# print(response8.json())
# response9 = requests.patch(BASE + "list_event_details/3", {"user_id": 1})
# print(response9.json())
#
# response10 = requests.put(BASE + "list_event_details/5", {"new_task": "Garbage",
#                                                           "new_description": "Take the garbage out please"})
# print(response10.json())

if __name__ == '__main__':
    unittest.main()
