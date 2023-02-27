"""Endpoints for transactions"""
import flask_restful  # type: ignore

import server.transactions.ledger_resource
import server.transactions.transaction_resources as tr


def attach(api: flask_restful.Api):
    """Attaches all endpoints to the flask app"""
    api.add_resource(tr.TransactionResource, "/transaction/<int:t_id>", "/transaction")
    api.add_resource(server.transactions.ledger_resource.LedgerResource, "/ledger/<int:user_id>")
