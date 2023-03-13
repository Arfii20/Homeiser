from __future__ import annotations

from settle import flow, flow_algorithms
from transactions.transaction import Transaction

from dataclasses import dataclass
import json
from mysql.connector import cursor



class LedgerConstructionError(Exception):
    """Failed to create Ledger"""


@dataclass
class Ledger:
    """List of transactions. In JSON:
    '[{Transaction}, {Transaction}...{Transaction}]'
    """

    transactions: list[Transaction]

    @staticmethod
    def build_from_user_id(user_id: int, cur: cursor.MySQLCursor) -> Ledger:
        """Builds a ledger of transactions given a user id and a cursor to the db.
        Returns an empty ledger where user has no transactions
        """
        # validate user id; return a 404 if not found

        cur.execute("SELECT id FROM user where id = %s;", [user_id])
        if not cur.fetchall():
            raise LedgerConstructionError("User not found")

        # get all transaction ids where the user is src or dest
        cur.execute(
            "SELECT transaction.id FROM transaction, pairs "
            "WHERE pair_id = pairs.id AND (src = %s OR dest = %s)",
            [user_id, user_id],
        )

        # extract transaction ids
        transaction_rows = cur.fetchall()

        # throw an exception if no results were returned
        if not transaction_rows:
            raise LedgerConstructionError

        transaction_ids = [
            v for v in {tid[0] for tid in [row for row in transaction_rows]}
        ]

        return Ledger(
            [
                Transaction.build_from_id(transaction_id=t_id, cur=cur)
                for t_id in transaction_ids
            ]
        )

    @staticmethod
    def build_from_house_id(house_id: int, cur: cursor.MySQLCursor) -> Ledger:
        """Builds a ledger of all unsettled transactions in a house"""

        # validate that house id exists
        cur.execute(
            "SELECT household.id FROM household WHERE household.id = %s", [house_id]
        )

        if not cur.fetchall():
            raise LedgerConstructionError("Household not found")

        # get all unpaid transaction ids for the given household
        cur.execute(
            "SELECT transaction.id FROM transaction "
            "INNER JOIN pairs p on transaction.pair_id = p.id "
            "INNER JOIN user u on p.src = u.id "
            "INNER JOIN household h on h.id = u.household_id "
            "WHERE h.id = %s "
            "AND paid = 0;",
            [house_id],
        )

        transaction_rows = cur.fetchall()

        transaction_ids = [
            v for v in {tid[0] for tid in [row for row in transaction_rows]}
        ]

        return Ledger(
            [
                Transaction.build_from_id(transaction_id=t_id, cur=cur)
                for t_id in transaction_ids
            ]
        )

    @property
    def json(self):
        """Returns json; list of transactions"""
        return json.dumps([t.json for t in self.transactions])

    @property
    def users(self) -> list[tuple[int, str]]:
        """Returns a list of users ids and names"""
        u = set()
        for transaction in self.transactions:
            u.add((transaction.src_id, transaction.src_name))
            u.add((transaction.dest_id, transaction.dest_name))

        return [u_ for u_ in u]

    @staticmethod
    def simplify(household_id: int, cur: cursor.MySQLCursor) -> None:
        """Simplifies all unmarked transactions in a group.

        1. Pulls all open (i.e. unpaid) transactions of a house
        2. Converts transactions into flow graph vertices
        3. Runs simplification on the flow graph
        4a. If no simplifications were found, report no simplifications made
        4b. If there are simplifications to be made:
            * Check off simplifications with a 'bookmaker' user id (some reserved u_id; arbitrary)
            * Add new transactions from the simplified model
            * Return that transactions have been updated
        """

        # get ledger of all unmarked transactions in the house
        ledger = Ledger.build_from_house_id(household_id, cur)

