from flask_restful import Resource

from server import db_handler as db
from transactions.ledger import Ledger, LedgerConstructionError, SimplificationError


class LedgerResource(Resource):
    """Ledger is a list of transaction_resources.
    In JSON represented as '[t_1, t_2, ..., t_n]' where t_1..t_n are JSON(TransactionResource)
    """

    def get(self, user_id: int):
        """Given a user id, will return a 'ledger' of all user's transaction_resources whether they are src or dest"""
        try:
            ledger = Ledger.build_from_user_id(user_id, db.get_db())
            return ledger.json, 200

        except LedgerConstructionError:
            return "Could not return given user's transaction_resources", 404

    def post(self, house_id: int):
        """Simplifies ledger"""

        conn, cur = db.get_conn()

        try:
            l = Ledger.build_from_house_id(house_id, cur)
        except LedgerConstructionError:
            return f'Failed to access transactions for household {house_id}'

        try:
            l.simplify(house_id, cur, conn)
            return 201
        except SimplificationError as se:
            return str(se), 500
