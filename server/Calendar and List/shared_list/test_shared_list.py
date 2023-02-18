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
                if response.json() == {"message": "List Created"}:
                    break
        file.close()
        requests.delete(f"{BASE}list_details/{number}")
        response = requests.post(BASE + "shared_list/1", {'id': number,
                                                          "name": word[0:len(word) - 2]})
        self.assertEqual(response.json(), {"message": "List Created"})

    def test_shared_list_get(self):
        response = requests.get(BASE + "shared_list/1")
        valid = True
        for i in response.json().keys():
            if i not in ['id', 'name', 'household_id']:
                valid = False
        self.assertTrue(valid)

    def test_shared_list_get_bad(self):
        response = requests.get(BASE + "shared_list/2")
        self.assertEqual(response.json(), {'id': [], 'name': [], 'household_id': []})


class TestListDetails(unittest.TestCase):

    def test_list_delete(self):
        file = open("words.txt")
        words = file.readlines()
        file_length = len(words) - 1
        while True:
            word = words[randint(0, file_length)]
            number = randint(0, 5000)
            if len(word) > 4:
                response = requests.post(BASE + "shared_list/1", {'id': number,
                                                                  "name": word[0:len(word) - 2]})
                if response.json() == {"message": "List Created"}:
                    break
        file.close()
        response = requests.delete(f"{BASE}list_details/{number}")
        self.assertEqual(response.json(), {'message': 'List Deleted'})

    def test_list_delete_bad(self):
        response = requests.delete(f"{BASE}list_details/2")
        self.assertEqual(response.json(), {'message': 'List Doesnt Exist'})

    def test_list_patch(self):
        """
        Should work as name is unique and the row exists
        """
        response = requests.patch(BASE + "list_details/1", {"new_name": "Yameeen"})
        self.assertEqual(response.json(), {'message': 'Update Successful'})

    def test_list_patch_bad(self):
        """
        Should fail as name already exists and id does not exist
        """
        response = requests.patch(BASE + "list_details/40", {"new_name": "Yameen"})
        self.assertEqual(response.json(), {'error': 'List name already exists and id does not exist'})

    def test_list_patch_bad2(self):
        """
        Should fail as name already exists but id is valid
        """
        response = requests.patch(BASE + "list_details/52", {"new_name": "Yameen"})
        self.assertEqual(response.json(), {'error': 'List name already exists'})

    def test_list_patch_bad3(self):
        """
        Should fail as id does not exist but name is valid
        """
        response = requests.patch(BASE + "list_details/39", {"new_name": "Yameeeeen"})
        self.assertEqual(response.json(), {'error': 'List id does not exist'})


#
class TestListEvents(unittest.TestCase):
    def test_list_events_post(self):
        """
        To insert list event to the table
        """
        response = requests.post(BASE + "list_events/1", {"task_name": "Garbaage",
                                                          "description_of_task": "Take the garbage outside "
                                                                                 "before evening please",
                                                          "added_user_id": 1})
        self.assertEqual(response.json(), {'message': 'List Event Created'})

    def test_list_events_post_bad(self):
        """
        To insert list event to the table
        """
        response = requests.post(BASE + "list_events/1", {"event_id": 3,
                                                          "task_name": "Garbaage",
                                                          "description_of_task": "Take the garbage outside "
                                                                                 "before evening please",
                                                          "added_user_id": 1})
        self.assertEqual(response.json(), {'error': 'Event id already exists'})

    def test_list_events_get_good(self):
        """
        Gets all the events of a particular list
        """
        response = requests.get(BASE + "list_events/1")
        valid = True
        for i in response.json().keys():
            if i not in ['id', 'task_name', 'description_of_task', 'added_user_id', 'checked_off_by_user', 'list']:
                valid = False
        self.assertTrue(valid)

    def test_list_events_get_bad(self):
        """
        Should fail as list id does not exist
        """
        response = requests.get(BASE + "list_events/30")
        self.assertEqual(response.json(), {'error': 'List id not found'})


class ListEventDetails(unittest.TestCase):

    def test_list_events_delete(self):
        requests.post(BASE + "list_events/1", {"event_id": 69,
                                               "task_name": "Testing",
                                               "description_of_task": "Testing",
                                               "added_user_id": 3})
        response = requests.delete(BASE + "list_event_details/69")
        self.assertEqual(response.json(), {'message': 'List Event Deleted'})

    def test_list_events_checkoff_without_id_patch(self):
        requests.post(BASE + "list_events/1", {"event_id": 420,
                                               "task_name": "Testing",
                                               "description_of_task": "Testing",
                                               "added_user_id": 3})
        response = requests.patch(BASE + "list_event_details/420")
        requests.delete(BASE + "list_event_details/420")
        self.assertEqual(response.json(), {"error": "User ID required to check-off"})

    def test_list_events_checkoff_with_id_patch(self):
        requests.post(BASE + "list_events/1", {"event_id": 420,
                                               "task_name": "Testing",
                                               "description_of_task": "Testing",
                                               "added_user_id": 3})
        response = requests.patch(BASE + "list_event_details/420", {"user_id": 4})
        requests.delete(BASE + "list_event_details/420")
        self.assertEqual(response.json(), {"message": "Checked-off"})

    def test_list_events_un_check_with_id_patch(self):
        requests.post(BASE + "list_events/1", {"event_id": 420,
                                               "task_name": "Testing",
                                               "description_of_task": "Testing",
                                               "added_user_id": 3})
        requests.patch(BASE + "list_event_details/420", {"user_id": 4})
        response = requests.patch(BASE + "list_event_details/420")
        requests.delete(BASE + "list_event_details/420")
        self.assertEqual(response.json(), {"message": "Un-Checked"})

    def test_list_events_put_bad(self):
        requests.post(BASE + "list_events/1", {"event_id": 420,
                                               "task_name": "Testing",
                                               "description_of_task": "Testing",
                                               "added_user_id": 3})
        response = requests.put(BASE + "list_event_details/420", {"new_task": "Garbage",
                                                                  "new_description": "Take the garbage out please"})
        requests.delete(BASE + "list_event_details/420")
        self.assertEqual(response.json(), {"message": "Task details updated"})

    def test_list_events_put_good(self):
        requests.post(BASE + "list_events/1", {"event_id": 420,
                                               "task_name": "Testing",
                                               "description_of_task": "Testing",
                                               "added_user_id": 3})
        requests.delete(BASE + "list_event_details/420")
        response = requests.put(BASE + "list_event_details/420", {"new_task": "Garbage",
                                                                  "new_description": "Take the garbage out please"})
        self.assertEqual(response.json(), {"error": "Event not found"})


if __name__ == '__main__':
    unittest.main()
