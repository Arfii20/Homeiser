from flask_restful import Resource

class Transaction(Resource):
    def get(self):
        return {'hello': 'world'}