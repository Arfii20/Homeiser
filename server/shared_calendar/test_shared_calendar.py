import requests
import unittest

BASE = "http://127.0.0.1:5000/"


class TestSharedCalendar(unittest.TestCase):

    def test_shared_calendar_get(self):
        """
        Tests if received something
        """
        message = requests.get(BASE + "shared_calendar/1", {"starting_time": "2022-02-19 00:00:00",
                                                             "ending_time": "2024-02-19 00:00:00"})
        self.assertIsNotNone(message.json())

    def test_shared_calendar_get_good(self):
        """
        Tests if received object have the required keys
        """
        message = requests.get(BASE + "shared_calendar/1", {"starting_time": "2022-02-19 00:00:00",
                                                             "ending_time": "2024-02-19 00:00:00"})
        valid = True
        for i in message.json().keys():
            if i not in ['event_id', 'title_of_event', 'starting_time', 'ending_time',
                         'additional_notes', 'location_of_event', 'added_by']:
                valid = False
        self.assertTrue(valid)

    def test_shared_calendar_without_id_post(self):
        """
        Tests if event is added to the table
        Does not send any particular event id
        """
        message = requests.post(BASE + "shared_calendar/1", {"title_of_event": "Partyyy",
                                                              "starting_time": '2023-02-19 00:00:00',
                                                              "ending_time": '2023-02-19 20:00:00',
                                                              "additional_notes": "Bring your own booze",
                                                              "location_of_event": "22 Manila House",
                                                              "tagged_users": '4 5 3',
                                                              "added_by": 7})
        self.assertEqual(message.json(), {'message': 'Event Added'})

    def test_shared_calendar_with_id_post(self):
        """
        Tests if event is added to the table
        Sends particular event id
        """
        requests.delete(BASE + "calendar_event/1")
        message = requests.post(BASE + "shared_calendar/1", {"id": 1,
                                                              "title_of_event": "Party",
                                                              "starting_time": '2023-02-19 00:00:00',
                                                              "ending_time": '2023-02-19 20:00:00',
                                                              "additional_notes": "Bring your own booze",
                                                              "location_of_event": "22 Manila House",
                                                              "tagged_users": '1 3 4',
                                                              "added_by": 1
                                                              })
        self.assertEqual(message.json(), {'message': 'Event Added'})

    def test_shared_calendar_with_id_post_bad(self):
        """
        Tests if event is added to the table
        Sends particular event id but receives error as that id already exists
        """
        message = requests.post(BASE + "shared_calendar/1", {"id": 1,
                                                              "title_of_event": "Party",
                                                              "starting_time": '2023-02-19 00:00:00',
                                                              "ending_time": '2023-02-19 20:00:00',
                                                              "additional_notes": "Bring your own booze",
                                                              "location_of_event": "22 Manila House",
                                                              "tagged_users": '1 3 4',
                                                              "added_by": 1
                                                              })
        self.assertEqual(message.json(), {'message': 'Cannot use this ID. Already exists'})


class TestCalendarEvent(unittest.TestCase):

    def test_calendar_event_get(self):
        """
        Tests if the received json keys are valid
        """
        message = requests.get(BASE + "calendar_event/180")
        valid = True
        for i in message.json().keys():
            if i not in ['tagged_users', 'event_id', 'title_of_event', 'starting_time', 'ending_time',
                         'additional_notes', 'location_of_event', 'household_id', 'tagged_users', 'added_by']:
                valid = False
        self.assertTrue(valid)

    def test_calendar_event_get_good1(self):
        """
        Tests if the received json keys are valid
        """
        message = requests.get(BASE + "calendar_event/180")
        self.assertNotEqual(message.json(), {})

    def test_calendar_event_get_bad(self):
        """
        Tests if received json is empty
        """
        message = requests.get(BASE + "calendar_event/2")
        self.assertEqual(message.json(), {"error": "Event id does not exist"})

    def test_calendar_event_get_good(self):
        """
        Tests if received json is empty
        """
        message = requests.get(BASE + "calendar_event/50")
        self.assertEqual(message.json(), {"error": "Event id does not exist"})

    def test_calendar_event_put_good(self):
        """
        Tests if updating an event's details is successful
        """
        message = requests.put(BASE + "calendar_event/180", {"title_of_event": "Party",
                                                            "starting_time": '2023-02-19 00:00:00',
                                                            "ending_time": '2023-02-19 20:00:00',
                                                            "additional_notes": "Bring your own booze",
                                                            "location_of_event": "22 Manila House",
                                                            "tagged_users": "3 7",
                                                            "added_by": 5
                                                            })
        self.assertEqual(message.json(), {"message": "Task details updated"})

    def test_calendar_event_put_bad(self):
        """
        Tests if updating an event's details is successful
        """

        message = requests.put(BASE + "calendar_event/40", {"title_of_event": "Party",
                                                             "starting_time": '2023-02-19 00:00:00',
                                                             "ending_time": '2023-02-19 20:00:00',
                                                             "additional_notes": "Bring your own booze",
                                                             "location_of_event": "22 Manila House",
                                                             "tagged_users": "6 4",
                                                             "added_by": 4
                                                             })
        self.assertEqual(message.json(), {'message': 'Event does not exist'})

    def test_calendar_event_put_bad1(self):
        """
        Tests if updating an event's details is not successful
        Reason: start date is not formatted correctly
        """
        message = requests.put(BASE + "calendar_event/2", {"title_of_event": "Party",
                                                            "starting_time": '202-02-19 00:00:00',
                                                            "ending_time": '2023-02-19 20:00:00',
                                                            "additional_notes": "Bring your own booze",
                                                            "location_of_event": "22 Manila House",
                                                            "tagged_users": "5 4",
                                                            "added_by": 2
                                                            })
        self.assertEqual(message.json(), {'message': 'Format of date is wrong'})

    def test_calendar_event_put_bad2(self):
        """
        Tests if updating an event's details is not successful
        Reason: End date is not formatted correctly
        """
        message = requests.put(BASE + "calendar_event/2", {"title_of_event": "Party",
                                                            "starting_time": '2023-02-19 00:00:00',
                                                            "ending_time": '202-02-19 20:00:00',
                                                            "additional_notes": "Bring your own booze",
                                                            "location_of_event": "22 Manila House",
                                                            "tagged_users": "6 4",
                                                            "added_by": 4
                                                            })
        self.assertEqual(message.json(), {'message': 'Format of date is wrong'})

    def test_calendar_event_delete(self):
        """
        Tests if an event is deleted successfully
        """
        requests.post(BASE + "shared_calendar/1", {"id": 1,
                                                   "title_of_event": "Party",
                                                   "starting_time": '2023-02-19 00:00:00',
                                                   "ending_time": '2023-02-19 20:00:00',
                                                   "additional_notes": "Bring your own booze",
                                                   "location_of_event": "22 Manila House",
                                                   "tagged_users": "6 4",
                                                   "added_by": 4
                                                   })
        message = requests.delete(BASE + "calendar_event/1")
        self.assertEqual(message.json(), {'message': 'Calendar Event Deleted'})

    def test_calendar_event_delete_bad(self):
        """
        Tests if an event is deleted unsuccessfully
        Reason: Event does not exist
        """
        requests.post(BASE + "shared_calendar/1", {"id": 1,
                                                   "title_of_event": "Party",
                                                   "starting_time": '2023-02-19 00:00:00',
                                                   "ending_time": '2023-02-19 20:00:00',
                                                   "additional_notes": "Bring your own booze",
                                                   "location_of_event": "22 Manila House",
                                                   "tagged_users": "6 4",
                                                   "added_by": 4
                                                   })
        requests.delete(BASE + "calendar_event/1")
        message = requests.delete(BASE + "calendar_event/1")
        self.assertEqual(message.json(), {'message': 'Calendar Event Doesnt Exist'})


class UserColour(unittest.TestCase):
    def test_user_color_get(self):
        message = requests.get(BASE + "user_color/1")

        valid = True
        for i in message.json().keys():
            if i not in ['id', 'color']:
                valid = False

        self.assertTrue(valid)

    def test_user_color_get_bad(self):
        message = requests.get(BASE + "user_color/20")

        self.assertEqual(message.json(), {'error': "Users or household id not found"})


if __name__ == '__main__':
    unittest.main()
