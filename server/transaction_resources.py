"""List of all resources pertaining to transactions"""

from server.db_handler import get_db
from flask_restful import Resource, Api  # type: ignore

conn = get_db()

class Transaction(Resource):
    """
    JSON Format for a Transaction object. Query this endpoint for a **single** transaction

        {   "src": <str:src full name>,
            "dest": <str:dest full name>,
            "amount": <int:amount>,
            "description": <str:description>
            "due_date": <str:date string in format yyyy-mm-ddThh:mm:ss.xxxZ> where x is a millisecond, T denotes time
                                                                            # and Z shows (Z)ero offset from UTC
            "paid": <str:boolean>
        }

    """

    def get(self, t_id: int):
        """
        Gets a transaction by ID. ID is supplied in the URL.
        """
        conn._execute_query('SELECT * FROM transaction;')
        return {"Test": "Conn"}


    def post(self):
        """Post a new transaction. Require a transaction in the format specified above"""

    def patch(self, t_id: int):
        """Updates a transaction to toggle paid status"""

        # SQL query in form of UPDATE transaction SET paid = 1 - paid
        # if paid, 1-1 = 0; if not paid, 1-0 = 1


class Ledger(Resource):
    """Ledger is a list of transactions.
    In JSON represented as '[t_1, t_2, ..., t_n]' where t_1..t_n are JSON(Transaction)
    """

    def get(self, user_id: int):
        """Given a user id, will return a 'ledger' of all user's transactions whether they are src or dest"""


class CalendarTransactions(Resource):
    """Builds a calendar event out of transactions"""
