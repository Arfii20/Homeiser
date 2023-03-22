import unittest
from json import loads, dumps

import requests

BASE = "http://127.0.0.1:5000/"

class TestGetSharedCalendar(unittest.TestCase):
    def test_shared_calendar_get(self):
        """
        Tests if received something
        """
        response = requests.post(
            BASE + "get_shared_calendar/620",
            {
                "starting_time": "2027-02-19 00:00:00",
                "ending_time": "2029-02-19 00:00:00",
            },
        )
        self.assertEqual(response.json(), {"error": "No event found"})

    def test_shared_calendar_get_good(self):
        """
        Tests if received object have the required keys
        """
        response = requests.post(
            BASE + "get_shared_calendar/620",
            {
                "starting_time": "2022-02-19 00:00:00",
                "ending_time": "2024-02-19 00:00:00",
            },
        )
        response = loads(response.json())
        response = loads(response[0])
        valid = True
        for i in response.keys():
            if i not in [
                "event_id",
                "title_of_event",
                "starting_time",
                "ending_time",
                "additional_notes",
                "location_of_event",
                "household_id",
                "tagged_users",
                "added_by",
            ]:
                valid = False
        self.assertTrue(valid)


class TestSharedCalendar(unittest.TestCase):
    def test_shared_calendar_without_id_post(self):
        """
        Tests if event is added to the table
        Does not send any particular event id
        """
        response = requests.post(
            BASE + "shared_calendar/620",
            {
                "title_of_event": "event a",
                "starting_time": "2023-02-19 00:00:00",
                "ending_time": "2023-02-19 20:00:00",
                "additional_notes": "description here",
                "location_of_event": "location of event",
                "tagged_users": "630 631 632",
                "added_by": 630,
            },
        )
        self.assertEqual(response.json(), {"message": "Event Added"})

    def test_shared_calendar_with_id_post(self):
        """
        Tests if event is added to the table
        Sends particular event id
        """
        requests.delete(BASE + "calendar_event/649")
        response = requests.post(
            BASE + "shared_calendar/620",
            {
                "id": 649,
                "title_of_event": "event a",
                "starting_time": "2023-02-19 00:00:00",
                "ending_time": "2023-02-19 20:00:00",
                "additional_notes": "description here",
                "location_of_event": "location of event",
                "tagged_users": "630 631 632",
                "added_by": 630,
            },
        )
        self.assertEqual(response.json(), {"message": "Event Added"})

    def test_shared_calendar_with_id_post_bad(self):
        """
        Tests if event is added to the table
        Sends particular event id but receives error as that id already exists
        """
        response = requests.post(
            BASE + "shared_calendar/620",
            {
                "id": 649,
                "title_of_event": "event a",
                "starting_time": "2023-02-19 00:00:00",
                "ending_time": "2023-02-19 20:00:00",
                "additional_notes": "description here",
                "location_of_event": "location of event",
                "tagged_users": "630 631 632",
                "added_by": 630,
            },
        )
        self.assertEqual(
            response.json(), {"message": "Cannot use this ID. Already exists"}
        )


class TestCalendarEvent(unittest.TestCase):
    def test_calendar_event_get(self):
        """
        Tests if the received json keys are valid
        """
        response = requests.get(BASE + "calendar_event/640")
        response = loads(response.json())
        valid = True
        for i in response.keys():
            if i not in [
                "tagged_users",
                "event_id",
                "title_of_event",
                "starting_time",
                "ending_time",
                "additional_notes",
                "location_of_event",
                "household_id",
                "tagged_users",
                "added_by",
            ]:
                valid = False
        self.assertTrue(valid)

    def test_calendar_event_get_good1(self):
        """
        Tests if the received json keys are valid
        """
        response = requests.get(BASE + "calendar_event/640")
        self.assertNotEqual(response.json(), {})

    def test_calendar_event_get_bad(self):
        """
        Tests if received json is empty
        """
        response = requests.get(BASE + "calendar_event/1640")
        self.assertEqual(response.json(), {"error": "Event id does not exist"})

    def test_calendar_event_put_good(self):
        """
        Tests if updating an event's details is successful
        """
        response = requests.put(
            BASE + "calendar_event/642",
            {
                "title_of_event": "event a",
                "starting_time": "2023-02-19 00:00:00",
                "ending_time": "2023-02-19 20:00:00",
                "additional_notes": "description changed here",
                "location_of_event": "location of event changed",
                "tagged_users": "630 631 632",
                "added_by": 630,
            },
        )
        self.assertEqual(response.json(), {"message": "Task details updated"})

    def test_calendar_event_put_bad(self):
        """
        Tests if updating an event's details is successful
        """

        response = requests.put(
            BASE + "calendar_event/1640",
            {
                "title_of_event": "event a",
                "starting_time": "2023-02-19 00:00:00",
                "ending_time": "2023-02-19 20:00:00",
                "additional_notes": "description changed here",
                "location_of_event": "location of event changed",
                "tagged_users": "630 631 632",
                "added_by": 630,
            },
        )
        self.assertEqual(response.json(), {"message": "Event does not exist"})

    def test_calendar_event_put_bad1(self):
        """
        Tests if updating an event's details is not successful
        Reason: start date is not formatted correctly
        """
        response = requests.put(
            BASE + "calendar_event/2",
            {
                "title_of_event": "event a",
                "starting_time": "202-02-19 00:00:00",
                "ending_time": "2023-02-19 20:00:00",
                "additional_notes": "description changed here",
                "location_of_event": "location of event changed",
                "tagged_users": "630 631 632",
                "added_by": 630,
            },
        )
        self.assertEqual(response.json(), {"message": "Format of date is wrong"})

    def test_calendar_event_put_bad2(self):
        """
        Tests if updating an event's details is not successful
        Reason: End date is not formatted correctly
        """
        response = requests.put(
            BASE + "calendar_event/2",
            {
                "title_of_event": "event a",
                "starting_time": "2023-02-19 00:00:00",
                "ending_time": "203-02-19 20:00:00",
                "additional_notes": "description changed here",
                "location_of_event": "location of event changed",
                "tagged_users": "630 631 632",
                "added_by": 630,
            },
        )
        self.assertEqual(response.json(), {"message": "Format of date is wrong"})

    def test_calendar_event_delete(self):
        """
        Tests if an event is deleted successfully
        """
        requests.post(
            BASE + "shared_calendar/620",
            {
                "id": 649,
                "title_of_event": "event a",
                "starting_time": "2023-02-19 00:00:00",
                "ending_time": "2023-02-19 20:00:00",
                "additional_notes": "description changed here",
                "location_of_event": "location of event changed",
                "tagged_users": "630 631 632",
                "added_by": 630,
            },
        )
        response = requests.delete(BASE + "calendar_event/649")
        self.assertEqual(response.json(), {"message": "Calendar Event Deleted"})

    def test_calendar_event_delete_bad(self):
        """
        Tests if an event is deleted unsuccessfully
        Reason: Event does not exist
        """
        requests.post(
            BASE + "shared_calendar/620",
            {
                "id": 676,
                "title_of_event": "event a",
                "starting_time": "2023-02-19 00:00:00",
                "ending_time": "2023-02-19 20:00:00",
                "additional_notes": "description changed here",
                "location_of_event": "location of event changed",
                "tagged_users": "630 631 632",
                "added_by": 630,
            },
        )
        requests.delete(BASE + "calendar_event/676")
        response = requests.delete(BASE + "calendar_event/676")
        self.assertEqual(response.json(), {"message": "Calendar Event Doesnt Exist"})


class UserAttributes(unittest.TestCase):
    def test_user_color_get(self):
        response = requests.get(BASE + "user_attributes/620")

        valid = True
        for i in response.json().keys():
            if i not in ["id", "color"]:
                valid = False

        self.assertTrue(valid)

    def test_user_color_get_bad(self):
        response = requests.get(BASE + "user_attributes/1620")

        self.assertEqual(response.json(), {"error": "Users or household id not found"})

    def test_user_id_post(self):
        response = requests.post(BASE + "user_attributes/620", {"names": "a b c"})

        self.assertListEqual(loads(response.json()), [630, 631, 632])


if __name__ == "__main__":
    unittest.main()
