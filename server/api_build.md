# Building APIs

## Documentation
Flask:  https://flask.palletsprojects.com/en/2.2.x/
Flask restful: https://flask-restful.readthedocs.io/en/latest/
unittest: https://docs.python.org/3/library/unittest.html


There are two main components to the API - resources and endpoints. Endpoints are the points where someone interacts
with the API. Resources are (sort of) classes which hold the code which is run when a user interacts with an endpoint



## Resources


Import `Resource` from `flask_restful` 
```python3 
from flask_restful import Resource 
```

Make a class that inherits from Resource and define methods which are named like the HTTP methods you want to implement.
For example, if you want code to be run when the endpoint receives a GET request, place the code in a method called `get`.

Getting a household requires you to have some way of telling the 


```python3
from flask_restful import Resource


class Household(Resource):
    
    def get(self, id: int):
        # some code
        return {"some": f"data {id}"}, 200
```

`get` returns `{"some": "data {id}"}` and a `200` status code. Return status codes so we (the front end) know if something
broke. 

Rinse and repeat for everything.

## Endpoints

Add endpoints 
```python3
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

api.add_resource(Group, "/group/<int:id>")
```

This means that any time anyone interacts with /group/<id> using a get request they will receive  `{"some": "data {id}"}`
and a 200 status code.

Add more urls as you need