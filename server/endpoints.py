"""Endpoints for transactions"""
import flask_restful  # type: ignore

import server.transactions.ledger_resource
import server.transactions.transaction_resources as tr
import server.User_actions.user_actions as user


def attach(api: flask_restful.Api):
    """Attaches all endpoints to the flask app"""
    api.add_resource(tr.TransactionResource, "/transaction/<int:t_id>", "/transaction")
    api.add_resource(server.transactions.ledger_resource.LedgerResource, "/ledger/<int:user_id>")
    api.add_resource(user.RegisterUser, "/register_user")
    api.add_resource(user.LoginUser, "/login_user<int:user_id><string:password>")
    api.add_resource(user.RegisterHouse, "/register_house")
    api.add_resource(user.LoginHouse, "/login_house<int:house_id><string:password>")
