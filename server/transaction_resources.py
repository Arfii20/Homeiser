"""List of all resources pertaining to transactions"""

from flask_restful import Resource  # type: ignore

class Transaction(Resource):
    def get(self, id: int):
        return {"Hello": "World",
                "ID": id}, 200
