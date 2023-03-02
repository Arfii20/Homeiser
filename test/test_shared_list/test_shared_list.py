import unittest
import requests
from random import randint
from json import loads

# from shared_list import SharedList, ListDetails

BASE = "http://127.0.0.1:5000/"


class TestSharedList(unittest.TestCase):
    def test_shared_list_get(self):
        response = requests.get(BASE + "shared_list/620")
        response = loads(response.json())
        response = loads(response[0])
        valid = True
        for i in response.keys():
            if i not in ["id", "name", "household_id"]:
                valid = False
        self.assertTrue(valid)

    def test_shared_list_get_bad(self):
        response = requests.get(BASE + "shared_list/1620")
        self.assertEqual(response.json(), {"error": "No lists found"})

    def test_shared_list_name_post_bad(self):
        response = requests.post(BASE + "shared_list/620", {"name": "list c"})
        self.assertEqual(response.json(), {"error": "List Name Must Be Unique"})

    def test_shared_list_id_post_bad(self):
        file = open("../../server/shared_list/words.txt")
        words = file.readlines()
        file_length = len(words) - 1
        while True:
            word = words[randint(0, file_length)]
            response = requests.post(
                BASE + "shared_list/620", {"id": 651, "name": word[0: len(word) - 2]}
            )

            if response.json() != {"error": "List Name Must Be Unique"}:
                break
        file.close()

        response = requests.post(
            BASE + "shared_list/620", {"id": 651, "name": word[0: len(word) - 2]}
        )
        self.assertEqual(response.json(), {"error": "ID Must Be Unique"})

    def test_shared_list_post_good(self):
        file = open("../../server/shared_list/words.txt")
        words = file.readlines()
        file_length = len(words) - 1
        while True:
            word = words[randint(0, file_length)]
            number = randint(0, 5000)
            if len(word) > 4:
                response = requests.post(
                    BASE + "shared_list/621",
                    {"id": number, "name": word[0: len(word) - 2]},
                )
                if response.json() == {"message": "List Created"}:
                    break
        file.close()
        requests.delete(f"{BASE}list_details/{number}")
        response = requests.post(
            BASE + "shared_list/621", {"id": number, "name": word[0: len(word) - 2]}
        )
        self.assertEqual(response.json(), {"message": "List Created"})


class TestListDetails(unittest.TestCase):
    def test_list_delete(self):
        file = open("../../server/shared_list/words.txt")
        words = file.readlines()
        file_length = len(words) - 1
        while True:
            word = words[randint(0, file_length)]
            number = randint(0, 5000)
            if len(word) > 4:
                response = requests.post(
                    BASE + "shared_list/620",
                    {"id": number, "name": word[0: len(word) - 2]},
                )
                if response.json() == {"message": "List Created"}:
                    break
        file.close()
        response = requests.delete(f"{BASE}list_details/{number}")
        self.assertEqual(response.json(), {"message": "List Deleted"})

    def test_list_delete_bad(self):
        response = requests.delete(f"{BASE}list_details/1650")
        self.assertEqual(response.json(), {"error": "List Doesnt Exist"})

    def test_list_patch(self):
        """
        Should work as name is unique and the row exists
        """
        response = requests.patch(BASE + "list_details/651", {"new_name": "list b changed"})
        self.assertEqual(response.json(), {"message": "Update Successful"})

    def test_list_patch_bad(self):
        """
        Should fail as name already exists and id does not exist
        """
        response = requests.patch(BASE + "list_details/659", {"new_name": "list a"})
        self.assertEqual(
            response.json(), {"error": "List name already exists and id does not exist"}
        )

    def test_list_patch_bad2(self):
        """
        Should fail as name already exists but id is valid
        """
        response = requests.patch(BASE + "list_details/655", {"new_name": "list d"})
        self.assertEqual(response.json(), {"error": "List name already exists"})

    def test_list_patch_bad3(self):
        """
        Should fail as id does not exist but name is valid
        """
        response = requests.patch(BASE + "list_details/659", {"new_name": "list j changed"})
        self.assertEqual(response.json(), {"error": "List id does not exist"})


class TestListEvents(unittest.TestCase):
    def test_list_events_post(self):
        """
        To insert list event to the table
        """
        response = requests.post(
            BASE + "list_events/652",
            {
                "task_name": "task h",
                "description_of_task": "description h",
                "added_user_id": 633
            }
        )
        self.assertEqual(response.json(), {"message": "List Event Created"})

    def test_list_events_post_bad(self):
        """
        To insert list event to the table
        """
        response = requests.post(
            BASE + "list_events/651",
            {
                "event_id": 661,
                "task_name": "task g",
                "description_of_task": "description g",
                "added_user_id": 631
            }
        )
        self.assertEqual(response.json(), {"error": "Event id already exists"})

    def test_list_events_get_good(self):
        """
        Gets all the events of a particular list
        """
        response = requests.get(BASE + "list_events/650")
        response = loads(response.json())
        response = loads(response[0])

        valid = True
        for i in response.keys():
            if i not in [
                "id",
                "task_name",
                "description_of_task",
                "added_user_id",
                "checked_off_by_user",
                "list",
            ]:
                valid = False
        self.assertTrue(valid)

    def test_list_events_get_bad(self):
        """
        Should fail as list id does not exist
        """
        response = requests.get(BASE + "list_events/1651")
        self.assertEqual(response.json(), {"error": "List id not found"})


class ListEventDetails(unittest.TestCase):
    def test_list_events_delete(self):
        requests.post(
            BASE + "list_events/650",
            {
                "event_id": 669,
                "task_name": "task g",
                "description_of_task": "description g",
                "added_user_id": 631
            }
        )
        response = requests.delete(BASE + "list_event_details/669")
        self.assertEqual(response.json(), {"message": "List Event Deleted"})

    def test_list_events_checkoff_without_id_patch(self):
        requests.post(
            BASE + "list_events/650",
            {
                "event_id": 669,
                "task_name": "task g",
                "description_of_task": "description g",
                "added_user_id": 631,
            }
        )
        response = requests.patch(BASE + "list_event_details/669")
        requests.delete(BASE + "list_event_details/669")
        self.assertEqual(response.json(), {"error": "User ID required to check-off"})

    def test_list_events_checkoff_with_id_patch(self):
        requests.post(
            BASE + "list_events/650",
            {
                "event_id": 669,
                "task_name": "task g",
                "description_of_task": "description g",
                "added_user_id": 631,
            }
        )
        response = requests.patch(BASE + "list_event_details/669", {"user_id": 631})
        requests.delete(BASE + "list_event_details/669")
        self.assertEqual(response.json(), {"message": "Checked-off"})

    def test_list_events_un_check_with_id_patch(self):
        requests.post(
            BASE + "list_events/650",
            {
                "event_id": 669,
                "task_name": "task g",
                "description_of_task": "description g",
                "added_user_id": 631,
            }
        )
        requests.patch(BASE + "list_event_details/669", {"user_id": 631})
        response = requests.patch(BASE + "list_event_details/669")
        requests.delete(BASE + "list_event_details/669")
        self.assertEqual(response.json(), {"message": "Un-Checked"})

    def test_list_events_put_good(self):
        requests.post(
            BASE + "list_events/650",
            {
                "event_id": 669,
                "task_name": "task g",
                "description_of_task": "description g",
                "added_user_id": 631,
            }
        )
        response = requests.put(
            BASE + "list_event_details/669",
            {"new_task": "task h", "new_description": "description h"},
        )
        requests.delete(BASE + "list_event_details/669")
        self.assertEqual(response.json(), {"message": "Task details updated"})

    def test_list_events_put_bad(self):
        requests.post(
            BASE + "list_events/650",
            {
                "event_id": 669,
                "task_name": "task g",
                "description_of_task": "description g",
                "added_user_id": 631,
            }
        )
        requests.delete(BASE + "list_event_details/669")
        response = requests.put(
            BASE + "list_event_details/669",
            {"new_task": "task h", "new_description": "description h"},
        )
        self.assertEqual(response.json(), {"error": "Event not found"})


if __name__ == "__main__":
    unittest.main()
