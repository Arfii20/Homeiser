from __future__ import annotations


from settle import flow, flow_algorithms
from transactions.transaction import Transaction

from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import logging
from mysql.connector import cursor

# initialise logger
logging.basicConfig(filename=f"{datetime.now()}.log", level=logging.INFO)
logger = logging.getLogger(__name__)


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

        # build a map of user ids to vertices for all users in graph
        users_vertices = {usr[0]: flow.Vertex(*usr) for usr in ledger.users}

        # build a graph including everyone in the household
        debt = flow.FlowGraph(vertices=[v for v in users_vertices.values()])

        # add an edge for every transaction in the graph
        for transaction in ledger.transactions:
            debt.add_edge(
                edge=flow.Edge(
                    users_vertices[transaction.dest_id], 0, transaction.amount
                ),
                src=users_vertices[transaction.src_id],
            )

        # debt.draw("pre_simplify", subdir='ledger', res=False)

        try:
            simplified = flow_algorithms.Settle.simplify_debt(debt)
        except flow_algorithms.NoSimplification as e:
            # log and propagate upwards
            logger.warning("No Simplifications found")
            raise e

        # otherwise
        #   1. build new ledger from flow graph
        #   2. delete old transactions
        #   3. add new transactions to db

        simplified.draw("simplified", subdir="ledger", res=False)

        simplified_ledger = Ledger([])

        # set new due date to today week
        new_due_date = datetime.today() + timedelta(days=7)

        for node, edges in simplified.graph.items():
            for edge in edges:
                # skip residual edges and edges
                if edge.residual:
                    continue
                # TODO: make an actual decision on due dates, default to a week today for now
                simplified_ledger.transactions.append(
                    Transaction(
                        0,
                        node.v_id,
                        edge.target.v_id,
                        node.label,
                        edge.target.label,
                        edge.capacity,
                        "Simplified Transaction",
                        new_due_date.date(),
                        False,
                        household_id,
                    )
                )

        print(simplified_ledger.transactions)
        print(len(simplified_ledger.transactions))
