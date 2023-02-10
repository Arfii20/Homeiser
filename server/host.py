"""Entry point for server"""

from flask import Flask
from flask_restful import Api
import mysql.connector

x5db = mysql.connector.connect(host="localhost", user="root", password="YOUR PASSWORD")

app = Flask(__name__)
api = Api(app)
