from flask_restful import Resource

from server import db_handler as db
from transactions.ledger import Ledger


class LedgerResource(Resource):
    """Ledger is a list of transactions.
    In JSON represented as '[t_1, t_2, ..., t_n]' where t_1..t_n are JSON(TransactionResource)
    """

    def get(self, user_id: int):
        """Given a user id, will return a 'ledger' of all user's transactions whether they are src or dest"""
        return Ledger.build_from_id(user_id, db.get_db()).json, 200
