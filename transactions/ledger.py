from __future__ import annotations

import sys

from settle import flow, flow_algorithms
from transactions.transaction import Transaction, TransactionInsertionFailed, CalendarEvent

from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import logging
from mysql.connector import cursor, MySQLConnection

# initialise logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)


class LedgerConstructionError(Exception):
    """Failed to create Ledger"""


class SimplificationError(Exception):
    ...


@dataclass
class Ledger:
    """List of transaction_resources. In JSON:
    '[{Transaction}, {Transaction}...{Transaction}]'
    """

    transactions: list[Transaction]

    @staticmethod
    def build_from_user_id(user_id: int, cur: cursor.MySQLCursor) -> Ledger:
        """Builds a ledger of transaction_resources given a user id and a cursor to the db.
        Returns an empty ledger where user has no transaction_resources
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
        """Builds a ledger of all unsettled transaction_resources in a house"""

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
        """Returns json; list of transaction_resources"""
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
    def simplify(
        household_id: int, cur: cursor.MySQLCursor, conn: MySQLConnection
    ) -> None:
        """Simplifies all unmarked transaction_resources in a group.

        1. Pulls all open (i.e. unpaid) transaction_resources of a house
        2. Converts transaction_resources into flow graph vertices
        3. Runs simplification on the flow graph
        4a. If no simplifications were found, report no simplifications made
        4b. If there are simplifications to be made:
            * Check off simplifications with a 'bookmaker' user id (some reserved u_id; arbitrary)
            * Add new transaction_resources from the simplified model
            * Return that transaction_resources have been updated
        """

        # get ledger of all unmarked transaction_resources in the house
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
        #   2. delete old transaction_resources
        #   3. add new transaction_resources to db

        simplified.draw("simplified", subdir="ledger", res=False)

        # build new ledger
        simplified_ledger = Ledger([])

        # set new due date to today week
        new_due_date = datetime.today() + timedelta(days=7)

        for node, edges in simplified.graph.items():
            for edge in edges:
                # skip residual edges and edges
                if edge.residual:
                    continue
                # TODO: make an actual decision on due dates, default to a week today for now
                logger.info(
                    f"Adding a transaction to the database: "
                    f"{node.label}--[{edge.capacity}]--> {edge.target.label}"
                )
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

        # try to insert new transaction_resources
        try:
            for transaction in simplified_ledger.transactions:
                transaction.insert_transaction(cur, conn)
        except TransactionInsertionFailed:
            # means something failed so remove anything that may have been added and add back old transaction_resources
            for t_id in [t.t_id for t in simplified_ledger.transactions]:
                cur.execute("""DELETE FROM transaction WHERE id = %s""", [t_id])

            raise SimplificationError(
                "Found a way to simplify debts; failed to execute. Try again later"
            )

        # delete old transaction_resources only if we have successfully added new ones
        for t_id in [t.t_id for t in ledger.transactions]:
            cur.execute("""DELETE FROM transaction WHERE id = %s""", [t_id])

        # commit
        conn.commit()

    def as_events(self) -> list[CalendarEvent]:
        """Converts transactions into calendar event objects"""
        return [CalendarEvent.from_transaction(t) for t in self.transactions]