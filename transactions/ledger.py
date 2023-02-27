from __future__ import annotations

import json
from dataclasses import dataclass

from mysql.connector import cursor

from transactions.transaction import Transaction


class LedgerConstructionError(Exception):
    """Failed to create Ledger"""


@dataclass
class Ledger:
    """List of transactions. In JSON:
    '[{Transaction}, {Transaction}...{Transaction}]'
    """

    transactions: list[Transaction]

    @staticmethod
    def build_from_id(user_id: int, cur: cursor.MySQLCursor) -> Ledger:
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

        return Ledger([Transaction.build_from_id(transaction_id=t_id, cur=cur) for t_id in transaction_ids])  # type: ignore

    @property
    def json(self):
        """Returns json; list of transactions"""
        return json.dumps([t.json for t in self.transactions])
