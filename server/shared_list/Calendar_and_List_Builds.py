import json


class CalendarEventBuild:
    def __init__(self, event: tuple, tagged_user: list, added_by: int):
        self.event_id = event[0]
        self.title_of_event = event[1]
        self.starting_time = (
            f"{event[2].year}-{event[2].month}-{event[2].day} "
            f"{event[2].hour}:{event[2].minute}:{event[2].second}"
        )
        self.ending_time = (
            f"{event[3].year}-{event[3].month}-{event[3].day} "
            f"{event[3].hour}:{event[3].minute}:{event[3].second}"
        )
        self.additional_notes = event[4]
        self.location_of_event = event[5]
        self.household_id = event[6]
        self.tagged_users = tagged_user
        self.added_by = added_by

    def build_calendar_event(self):
        dump = json.dumps(
            {
                "event_id": self.event_id,
                "title_of_event": self.title_of_event,
                "starting_time": self.starting_time,
                "ending_time": self.ending_time,
                "additional_notes": self.additional_notes,
                "location_of_event": self.location_of_event,
                "household_id": self.household_id,
                "tagged_users": self.tagged_users,
                "added_by": self.added_by,
            }
        )
        return dump


class ListBuild:
    def __init__(self, list_in: tuple):
        self.id = list_in[0]
        self.name = list_in[1]
        self.household_id = list_in[2]

    def build_list(self):
        dump = json.dumps(
            {"id": self.id, "name": self.name, "household_id": self.household_id}
        )
        return dump


class ListEventBuild:
    def __init__(self, event: tuple):
        self.event_id = event[0]
        self.task_name = event[1]
        self.description = event[2]
        self.added_user = event[3]
        self.checked_off_by_user = event[4]
        self.list_id = event[5]

    def build_list_event(self):
        dump = json.dumps(
            {
                "id": self.event_id,
                "task_name": self.task_name,
                "description_of_task": self.description,
                "added_user_id": self.added_user,
                "checked_off_by_user": self.checked_off_by_user,
                "list": self.list_id,
            }
        )
        return dump
