"""List of all resources pertaining to transaction_resources"""
import json

import mysql.connector
from flask import request
from flask_restful import Resource, Api  # type: ignore
from mysql.connector import cursor

import server.db_handler as db
from transactions.transaction import (
    Transaction,
    TransactionConstructionError,
    TransactionInsertionFailed,
)

import transactions.ledger as ledger


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

        conn, cur = db.get_conn()
        r = request.get_json()

        if type(r) is str:
            r = json.loads(r)

        # validate json by trying to build a transaction object from it; throw an exception if this fails
        try:
            trn = Transaction.build_from_req(request=r)
        except TransactionConstructionError:
            return "Incorrect JSON Format for Transaction object", 400

        try:
            trn.insert_transaction(cur, conn)
        except TransactionInsertionFailed:
            return json.dumps("Adding transaction failed"), 500

        return trn.json, 201

    def patch(self, t_id: int):
        """Updates a transaction to toggle paid status"""

        conn: mysql.connector.MySQLConnection
        cur: cursor.MySQLCursor

        conn, cur = db.get_conn()
        conn.commit()
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
        conn: mysql.connector.MySQLConnection
        cur: cursor.MySQLCursor

        conn, cur = db.get_conn()
        cur.execute("SELECT id FROM transaction WHERE id = %s", [t_id])
        if cur.fetchone() is None:
            return "Transaction not found; cannot be deleted", 402

        cur.execute("DELETE FROM transaction WHERE id = %s", [t_id])
        conn.commit()

        cur.execute("SELECT pair_id FROM transaction WHERE id = %s", [t_id])
        result = cur.fetchone()

        if result is not None:
            return f"Transaction {t_id} not deleted", 500
        else:
            return f"Deleted transaction {t_id}", 200


class CalendarTransactions(Resource):
    """Return user's transactions as calendar events"""

    def get(self, user_id: int):

        cur = db.get_db()

        # build ledger of user's transactions
        try:
            user_ledger = ledger.Ledger.build_from_user_id(user_id, cur)
        except ledger.LedgerConstructionError:
            return f"Internal Server Error - Could not get transactions for user_id {user_id}", 500

        # represent each transaction as a calendar event (using json). Have all transactions in a list and return
        events_json = json.dumps([event.json for event in user_ledger.as_events()])

        return events_json, 200