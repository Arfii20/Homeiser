"""List of all resources pertaining to transactions"""
import json

from flask_restful import Resource, Api  # type: ignore
import server.db_handler as db
from transactions.transaction import Transaction, TransactionConstructionError


class TransactionResource(Resource):
    """
    JSON Format for a TransactionResource object. Query this endpoint for a **single** transaction

        {   "transaction_id": <int:transaction id>
            "src_id": <int: src id>
            "src_id": <int: dest id>
            "src": <str:src full name>,
            "dest": <str:dest full name>,
            "amount": <int:amount>,
            "description": <str:description>
            "due_date": <str:date string in format yyyy-mm-dd>
            "paid": <str:boolean>
        }

    """

    def get(self, t_id: int):
        """
        Gets a transaction by ID. ID is supplied in the URL.
        """
        cur = db.get_db()

        try:
            trn = Transaction.build_from_id(transaction_id=t_id, cur=cur)
            return trn.json, 200
        except TransactionConstructionError as tre:
            return f"{tre}", 404

    def post(self):
        """Post a new transaction. Require a transaction in the format specified above (transaction_id not necessary)"""

    def patch(self, t_id: int):
        """Updates a transaction to toggle paid status"""

        # SQL query in form of UPDATE transaction SET paid = 1 - paid
        # if paid, 1-1 = 0; if not paid, 1-0 = 1

    def delete(self, t_id: int):
        ...


class Ledger(Resource):
    """Ledger is a list of transactions.
    In JSON represented as '[t_1, t_2, ..., t_n]' where t_1..t_n are JSON(TransactionResource)
    """

    def get(self, user_id: int):
        """Given a user id, will return a 'ledger' of all user's transactions whether they are src or dest"""


class CalendarTransactions(Resource):
    """Builds a calendar event out of transactions"""
