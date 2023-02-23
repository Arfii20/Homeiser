from __future__ import annotations

import json
from dataclasses import dataclass
from mysql.connector import cursor
from transactions.transaction import Transaction

@dataclass
class Ledger:
    transactions: list[Transaction]

    @staticmethod
    def build_from_id(user_id: int, cur: cursor.MySQLCursor) -> Ledger:
        """Builds a ledger of transactions given a user id and a cursor to the db"""

        cur.execute(
            "SELECT transaction.id FROM transaction, pairs "
            "WHERE pair_id = pairs.id AND (src = %s OR dest = %s)",
            [user_id, user_id],
        )

        # FIXME: statement returning duplicate ids e.g. returned 1, 1, 2

        transaction_ids = [
            v for v in {tid[0] for tid in [row for row in cur.fetchall()]}
        ]

        return Ledger([Transaction.build_from_id(transaction_id=t_id, cur=cur) for t_id in transaction_ids])  # type: ignore

    @property
    def json(self):
        """Returns json; list of transactions"""
        return json.dumps([t.json for t in self.transactions])
