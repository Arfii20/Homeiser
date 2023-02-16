import server.transaction_resources as tr
import server.host as host

host.api.add_resource(tr.Transaction, "/", "/transaction")
