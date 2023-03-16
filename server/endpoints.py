"""Endpoints for transaction_resources"""
import flask_restful  # type: ignore

import server.transaction_resources.ledger_resource as lr
import server.transaction_resources.transaction_resources as tr


def attach(api: flask_restful.Api):
    """Attaches all endpoints to the flask app"""
    api.add_resource(tr.TransactionResource, "/transaction/<int:t_id>", "/transaction")
    api.add_resource(lr.LedgerResource, "/ledger/<int:user_id>")
    api.add_resource(tr.CalendarTransactions, '/transaction/as_events/<int:user_id>')
