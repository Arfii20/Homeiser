"""Endpoints for transactions"""
import server.transaction_resources as tr
import flask_restful # type: ignore


def attach(api: flask_restful.Api):
    """Attaches all endpoints to the flask app"""
    api.add_resource(tr.TransactionResource, "/transaction/<int:t_id>", "/transaction")
    api.add_resource(tr.LedgerResource, "/ledger/<int:user_id>")
