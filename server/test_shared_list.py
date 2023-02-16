import unittest
import requests

# from shared_list import SharedList, ListDetails

BASE = "http://127.0.0.1:5000/"

# class TestSharedList(unittest.TestCase):
# def test_post(self):
#     returned = shared_list.


# List
response = requests.post(BASE + "shared_list/1", {"name": "Grortgc3e2s"})
print(response.json())

response1 = requests.get(BASE + "shared_list/1")
print(response1.json())

response2 = requests.delete(BASE + "list_details/97")
print(response2.json())

response3 = requests.patch(BASE + "list_details/54", {"new_name": "Yameen"})
print(response3.json())

# List Items
response4 = requests.post(BASE + "list_events/1", {"task_name": "Garbaage",
                                                   "description_of_task": "Take the garbage outside "
                                                                          "before evening please",
                                                   "added_user_id": 1})
print(response4.json())

response5 = requests.get(BASE + "list_events/1")
print(response5.json())

response6 = requests.delete(BASE + "list_event_details/2")
print(response6.json())

response7 = requests.patch(BASE + "list_event_details/3", {"user_id": 1})
print(response7.json())
response8 = requests.patch(BASE + "list_event_details/3", {"user_id": 1})
print(response8.json())
response9 = requests.patch(BASE + "list_event_details/3", {"user_id": 1})
print(response9.json())

response10 = requests.put(BASE + "list_event_details/5", {"new_task": "Garbage",
                                                          "new_description": "Take the garbage out please"})
print(response10.json())

response = requests.post(BASE + "shared_calendar/1", {"title_of_event": "Party",
                                                      "starting_time": "2023-02-25 20:00:00",
                                                      "ending_time": "2023-02-26 02:00:00",
                                                      "additional_notes": "Bring your own booze",
                                                      "location_of_event": "22 Manila House",
                                                      })
# print(response.json())


if __name__ == '__main__':
    unittest.main()
