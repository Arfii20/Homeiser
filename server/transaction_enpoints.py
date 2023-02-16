import server.transaction_resources as tr
import server.host as host

def attach():
    """Attaches all endpoints to app. Needs to be called from server/host"""
    host.api.add_resource(tr.Transaction, "/", "/transaction")
