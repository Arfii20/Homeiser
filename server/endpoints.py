"""Endpoints for transaction_resources"""
import flask_restful  # type: ignore

import server.transaction_resources.ledger_resource as lr
import server.transaction_resources.transaction_resources as tr
import server.shared_calendar.shared_calendar as calendar
import server.shared_list.shared_list as lists
import server.user_admin.user_resources as usr


def attach(api: flask_restful.Api):
    """Attaches all endpoints to the flask app"""

    # calendar
    api.add_resource(calendar.SharedCalendar, "/shared_calendar/<int:household_id>")
    api.add_resource(calendar.CalendarEvent, "/calendar_event/<int:calendar_event_id>")
    api.add_resource(calendar.UserColour, "/user_color/<int:household_id>")

    # list
    api.add_resource(lists.SharedList, "/shared_list/<int:household_id>")
    api.add_resource(lists.ListDetails, "/list_details/<int:list_id>")
    api.add_resource(lists.ListEvents, "/list_events/<int:list_id>")
    api.add_resource(lists.ListEventDetails, "/list_event_details/<int:list_event_id>")

    # transactions
    api.add_resource(tr.TransactionResource, "/transaction/<int:t_id>", "/transaction")
    api.add_resource(
        lr.LedgerResource, "/ledger/<int:user_id>", "/<int:house_id>/simplify"
    )
    api.add_resource(tr.CalendarTransactions, "/transaction/as_events/<int:user_id>")

    # users
    api.add_resource(usr.UserResource, "/user/<string:email>")
