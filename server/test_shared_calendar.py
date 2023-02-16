import requests
import datetime

# from shared_list import SharedList, ListDetails

BASE = "http://127.0.0.1:5000/"

# Calendar
# response = requests.post(BASE + "shared_calendar/1", {"title_of_event": "Party",
#                                                       "starting_time": [2023, 2, 25, 20, 00, 00],
#                                                       "ending_time": [2023, 2, 26, 2, 00, 00],
#                                                       "additional_notes": "Bring your own booze",
#                                                       "location_of_event": "22 Manila House",
#                                                       })
# print(response.json())

response1 = requests.get(BASE + "shared_calendar/1")
print(response1.json())

response1 = requests.get(BASE + "calendar_event/1")
print(response1.json())
#
# response2 = requests.put(BASE + "calendar_event/1", {"title_of_event": "Party",
#                                                      "starting_time": [2023, 2, 25, 20, 00, 00],
#                                                      "ending_time": [2023, 2, 26, 2, 00, 00],
#                                                      "additional_notes": "Bring your own booze",
#                                                      "location_of_event": "22 Manila House",
#                                                      })
# print(response2.json())


response1 = requests.delete(BASE + "calendar_event/1")
print(response1.json())

response1 = requests.get(BASE + "user_attributes/")
print(response1.json())