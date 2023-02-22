import json
import requests

exp = json.loads('{"transaction_id": 1, "src_id": 2, "dest_id": 1, "src": "Alice _", "dest": "Bob _", "amount": 20,'
                 ' "description": "test", "due_date": "2023-02-17", "paid": "false"}')

r = requests.post('http://127.0.0.1:5000/transaction', json=exp)
print(r.json(), r.status_code)

