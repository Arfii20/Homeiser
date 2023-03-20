import datetime
import json
from dataclasses import dataclass

@dataclass
class User:
    u_id: int
    first_name: str
    surname: str
    email: str
    password: bytes
    dob: datetime.date
    household: int
    colour: int

    def insert_to_database(self): ...

    def join_household(self, house: int): ...

    def leave_household(self, house: int): ...

    def delete(self): ...

    @staticmethod
    def build_from_email(email: str): ...

    @staticmethod
    def build_from_id(u_id: int): ...

    @property
    def json(self):
        return json.dumps(
            {"user_id": self.u_id,
             "first_name": self.first_name,
             "surname": self.surname,
             "email": self.email,
             "password": str(self.password, encoding='utf-8'),
             "dob": self.dob.isoformat(),
             "household_id": self.household,
             "colour": self.colour
             }
        )