"""Transaction Object"""
import json
from dataclasses import dataclass
import datetime
@dataclass
class Transaction:
    """Specifies a singular transaction"""
    t_id: int
    src_id: int
    dest_id: int
    amount: int
    due: datetime.datetime
    paid: bool
    description: str = ""
    src_name: str = ""
    dest_name: str = ""


    @property
    def json(self) -> str:
        """Returns a JSON representation of transaction object of the format

         {   "src": <str:src full name>,
            "dest": <str:dest full name>,
            "amount": <int:amount>,
            "description": <str:description>
            "due_date": <str:date string in format yyyy-mm-ddThh:mm:ss.xxxxxx> where x is a millisecond, T denotes time
            "paid": <str:boolean>
        }

        """

        return json.dumps({
            "src": self.src_name,
            "dest": self.dest_name,
            "amount": self.amount,
            "description": self.description,
            "due_date": self.due.isoformat(),
            "paid": "true" if self.paid else "false"
        })