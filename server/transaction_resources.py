"""List of all resources pertaining to transactions"""
import json

from flask import request
from flask_restful import Resource, Api  # type: ignore
import server.db_handler as db
from transactions.transaction import Transaction, TransactionConstructionError
from transactions.ledger import Ledger


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
        """Post a new transaction. Require a transaction in the format specified above (transaction_id not necessary).
        Returns json of the object added (with correct ID)"""

        cur = db.get_db()
        r = request.get_json()

        if type(r) is str:
            r = json.loads(r)

        # validate json by trying to build a transaction object from it; throw an exception if this fails
        try:
            _ = Transaction.build_from_req(request=r)
        except TransactionConstructionError:
            return "Incorrect JSON Format for Transaction object", 400

        # get pair id
        cur.execute(
            "SELECT id FROM pairs WHERE src = %s AND dest = %s",
            [r["src_id"], r["dest_id"]],
        )
        pair_id = cur.fetchone()

        # add pair to pairs table if the pair doesn't already exist
        if pair_id is None:
            cur.execute(
                "INSERT INTO pairs(src, dest) VALUES (%s, %s)",
                [r["src_id"], r["dest_id"]],
            )

            # get id from pair entry that was just generated
            cur.execute(
                "SELECT id FROM pairs WHERE src = %s AND dest = %s",
                [r["src_id"], r["dest_id"]],
            )
            pair_id = cur.fetchone()

            # commit changes
            cur.execute("commit;")

        # unpack pair_id from tuple
        pair_id = pair_id[0]

        # construct Transaction object from the request
        try:
            trn = Transaction.build_from_req(request=r)
        except TransactionConstructionError:
            return "Incorrect JSON Format for Transaction object", 400

        # insert new Transaction object into the database
        cur.execute(
            "INSERT INTO transaction(pair_id, amount, description, due_date, paid) "
            "VALUES (%s, %s, %s, %s, %s)",
            [
                pair_id,
                trn.amount,
                trn.description,
                trn.due.isoformat(),
                1 if trn.paid else 0,
            ],
        )

        # update the id of the new transaction
        cur.execute(
            "SELECT id FROM transaction WHERE pair_id = %s AND amount = %s AND due_date = %s AND paid = %s",
            [pair_id, r["amount"], r["due_date"], 1 if r["paid"] == "true" else 0],
        )

        # update trn to have the correct ID
        trn.t_id = cur.fetchone()[0]

        # commit changes
        cur.execute("commit;")

        return trn.json, 201

    def patch(self, t_id: int):
        """Updates a transaction to toggle paid status"""

        cur = db.get_db()
        result = cur.execute(
            "UPDATE transaction SET paid = 1 - paid WHERE id = %s; commit", [t_id]
        )

        # SQL query in form of UPDATE transaction SET paid = 1 - paid
        # if paid, 1-1 = 0; if not paid, 1-0 = 1

        if result is not None:
            return f"Marked {t_id} as paid", 200
        else:
            return f"Transaction {t_id} doesn't exist", 404

    def delete(self, t_id: int):
        cur = db.get_db()
        result = cur.execute("DELETE FROM transaction WHERE id = %s; commit", [t_id])

        if result is None:
            return f"Transaction {t_id} not found", 404
        else:
            return f"Deleted transaction {t_id}", 200


class LedgerResource(Resource):
    """Ledger is a list of transactions.
    In JSON represented as '[t_1, t_2, ..., t_n]' where t_1..t_n are JSON(TransactionResource)
    """

    def get(self, user_id: int):
        """Given a user id, will return a 'ledger' of all user's transactions whether they are src or dest"""
        return Ledger.build_from_id(user_id, db.get_db()).json, 200


class CalendarTransactions(Resource):
    """Builds a calendar event out of transactions"""
