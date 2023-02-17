"""Endpoints for transactions"""
import transaction_resources as tr
import flask_restful


def attach(api: flask_restful.Api):
    """Attaches all endpoints to the flask app"""
    api.add_resource(tr.Transaction, "/<int:t_id>")