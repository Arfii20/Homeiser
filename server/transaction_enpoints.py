"""List of all endpoints pertaining to transactions"""

import transaction_resources as tr  # type: ignore
import host  # type: ignore
def attach():
    """Attaches all endpoints to app. Needs to be called from server/host"""
    host.api.add_resource(tr.Transaction, "/transaction/<int:id>")
