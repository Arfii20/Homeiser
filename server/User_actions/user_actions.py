from flask import Flask, redirect, url_for
from flask_restful import Resource, Api, reqparse, abort
from mysql.connector import connect
from server.host import *
import re
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import login_user, logout_user, LoginManager

# create an instance of Flask
app = Flask(__name__)

# create an instance of Flast RESTful API
api = Api(app)

# configure and get db
connection = connect(
    host="localhost",
    user="root",
    password="Computer123!",
    database="x5db",
)


class RegisterUser(Resource):
    """Create a new user """

    def post(self):
        """
        Creates a new user in the database by inserting a new row in user table

        Request if of the form: requests.post(BASE + "register_user/1", {"firstname": "FirstName", "surname":
        "Surname", "password":"password", "email":r'[^@]+@[^@]+\.[^@]+'", "date_of_birth": yyyy-mm-dd, "color":1}

        :returns:
        If successfully,
        {'message': 'User Created'}
        """
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int, location='form')
        parser.add_argument('first_name', type=str, help='First name is a required field', required=True,
                            location='form')
        parser.add_argument('surname', type=str, help='Surname is a required field', required=True, location='form')
        parser.add_argument('password1', type=str, help='Password is a required field', required=True, location='form')
        parser.add_argument('password2', type=str, help='Password must be entered twice for verification',
                            required=True, location='form')
        parser.add_argument('email', type=str, help='Email is a required field', required=True, location='form')
        parser.add_argument('date_of_birth', type=str, help='DOB is a required field', required=True, location='form')
        parser.add_argument('color', type=int, help='Color is a required field', required=True, location='form')

        args = parser.parse_args()
        user_id = args.get("id")
        first_name = args.get("first_name")
        surname = args.get("surname")
        date_of_birth = args.get("date_of_birth")
        color = args.get("color")
        email = args.get("email")

        # check if passwords are equal
        if args.get("password1") == args.get("password2"):
            password = args.get("password1")
            password = generate_password_hash(password, method='SHA256')    # generate password hash to be stored in database for security reasons
        else:
            abort(406, Error="Passwords do not match")

        email_account = None
        if email:  # try and get email from database to see if it exists
            cursor1 = connection.cursor()
            cursor1.execute("SELECT * FROM user WHERE email = '%s';" % email)
            email_account = cursor1.fetchone()

        user_account = None
        if user_id:  # try and get user_id from database to see if it exists
            cursor2 = connection.cursor()
            cursor2.execute("SELECT * FROM user WHERE id = %s;" % user_id)
            user_account = cursor2.fetchone()

        if email_account:
            abort(409, Error="Account already exists !")  # email already in use
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):  # email of the wrong format
            abort(409, Error="Invalid email address entered!")
        elif user_account:
            abort(409, Error="ID must be unique")  # user_id already exists
        else:
            insert_user = "INSERT INTO user(id,first_name, surname, password, email, date_of_birth, color) VALUES (%s, '%s', '%s', '%s', '%s', %s, %s);"
            data = (user_id, first_name, surname, password, email, date_of_birth, color)
            cursor = connection.cursor()
            cursor.execute(insert_user % data)
            connection.commit()
            return {"message": "User created successfully"}, 200

class LoginUser(Resource):
    """ Login into user account using specific user id
         requests.post(BASE + "login_user/1", {"email": "Email", "password":"Password"}
    """

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, location='form', required = True, help='Email is a required field')
        parser.add_argument('password', type=str, help='Password is a required field', required=True,
                            location='form')

        args = parser.parse_args()
        email = args.get("email")
        password_entered = args.get("password")
        if email:  # try and get email from database to see if it exists
            cursor1 = connection.cursor()
            cursor1.execute("SELECT email,password FROM user WHERE email = '%s';" % email)
            account = cursor1.fetchone()
            if account:
                if check_password_hash(account.password, password_entered):
                    #login_user(account, remember=True)
                    return {"message": "Logged in successfully"}, 200
                else:
                    abort(409, Error="Incorrect password entered")
            else:
                abort(409, Error="Email does not exist")

class Logout(Resource):
    def logout(self):
        #logout_user()
        return {"message": "user successfully logged out"}

class UserDetails(Resource):
    def get(self, user_id, password):
        """Returns a list of a specific users details to website
        Get requests are of the form:
            requests.get(BASE + "login/")
        :returns
        Server returns the following json object:
            "id": [2],
            "first_name": ["name"],
            "surname": ["surname"],
            "password": ["password123"],
            "email": [hello@123.com],
            "date_of_birth": [2001-09-12],
            "household_id": [3],
            "color": [1]

        If no user that has that user_id, then list will return as empty and error message saying "No user found" returned
        """

        cursor = connection.cursor()

        query = "SELECT * FROM user WHERE id = %s AND password = '%s';"
        data = (user_id, password)
        cursor.execute(query % data)
        fetched_id = cursor.fetchall()

        if fetched_id:
            objects = {
                "id": [],
                "first_name": [],
                "surname": [],
                "password": [],
                "email": [],
                "date_of_birth": [],
                "household_id": [],
                "color": []
            }

            for i in cursor.fetchall():
                objects["id"].append(i[0])
                objects["first_name"].append(i[1])
                objects["surname"].append(i[2])
                objects["password"].append(i[3])
                objects["email"].append(i[4])
                objects["date_of_birth"].append(i[5])
                objects["household_id"].append(i[6])
                objects["color"].append(i[7])

            return objects, 200
        else:
            abort(404, error="No user found")


class RegisterHouse(Resource):
    """Register a new house"""

    def post(self):
        """
        Creates a new household in the database by inserting a new row in household table

        Request if of the form:
        requests,post(BASE + "register_house/1", {"firstname": "FirstName", "surname": "Surname", "password":"password", "email":r'[^@]+@[^@]+\.[^@]+'", "date_of_birth": yyyy-mm-dd, "color":1}

        :returns:
        If successfully created,
        {'message': 'Household Created'}
        """

        parser = reqparse.RequestParser()
        parser.add_argument('house_id', type=int, location='form')
        parser.add_argument('name', type=str, help='Name is a required field', required=True, location='form')
        parser.add_argument('password1', type=str, help='Password is a required field', required=True, location='form')
        parser.add_argument('password2', type=str, help='Password must be entered twice for verification',
                            required=True, location='form')
        parser.add_argument('max_residents', type=int, help='Max Residents is a required field', required=True,
                            location='form')
        parser.add_argument('postcode_id', type=int, location='form')
        parser.add_argument('postcode', type=str, help='Postcode is a required field', required=True, location='form')
        parser.add_argument('road_name', type=str, help='Road Name is a required field', required=True, location='form')

        args = parser.parse_args()

        house_id = args.get("house_id")
        name = args.get("name")
        postcode_id = args.get("postcode_id")
        postcode = args.get("postcode")
        road_name = args.get("road_name")
        max_residents = args.get("max_residents")


        # check if passwords are equal
        if args.get("password1") == args.get("password2"):
            password = args.get("password1")
            password = generate_password_hash(password, method='SHA256')    # generate password hash to be stored in database for security reasons
        else:
            abort(406, Error="Passwords do not match")

        postcode_account = None
        if postcode_id:  # try and get email from database to see if it exists
            cursor1 = connection.cursor()
            cursor1.execute("SELECT * FROM postcode WHERE id = %s;" % postcode_id)
            postcode_account = cursor1.fetchone()

        house_account = None
        if house_id:  # try and get user_id from database to see if it exists
            cursor2 = connection.cursor()
            cursor2.execute("SELECT * FROM household WHERE id = %s;" % house_id)
            house_account = cursor2.fetchone()

        if postcode_account:
            abort(409, Error="Postcode already exists !")  # postcode already in use
        elif house_account:
            abort(409, Error="House ID must be unique")  # house_id already exists
        else:
            insert_house = "INSERT INTO household(id,name,password, max_residents, postcode_id) VALUES (%s, '%s', '%s', %s, %s);"
            house_data = (house_id, name, password, max_residents, postcode_id)
            cursor = connection.cursor()
            cursor.execute(insert_house % house_data)
            connection.commit()

            insert_postcode = "INSERT INTO postcode(id, code, road_name) VALUES (%s, '%s', '%s');"
            postcode_data = (postcode_id, postcode, road_name)
            cursor3 = connection.cursor()
            cursor3.execute(insert_postcode % postcode_data)
            cursor3.commit()
            return {"message": "House created successfully"}, 200


class LoginHouse(Resource):
    """ login in to household"""

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='form', required=True, help='Name of house is a required field')
        parser.add_argument('password', type=str, help='Password is a required field', required=True,
                            location='form')

        args = parser.parse_args()
        name = args.get("name")
        password_entered = args.get("password")
        if name:  # try and get email from database to see if it exists
            cursor1 = connection.cursor()
            cursor1.execute("SELECT name,password FROM household WHERE name = '%s';" % name)
            house_account = cursor1.fetchone()
            if house_account:
                if check_password_hash(house_account.password, password_entered):
                    #login_user(house_account, remember=True)
                    return {"message": "Logged in successfully"}, 200
                else:
                    abort(406, Error="Incorrect password entered")
            else:
                abort(406, Error="House name does not exist")


api.add_resource(RegisterUser, "/register_user/")
api.add_resource(LoginUser, "/login_user<int:user_id><string:password>")
api.add_resource(RegisterHouse, "/register_house")
api.add_resource(LoginHouse, "/login_house<int:house_id><string:password>")

if __name__ == "__main__":
    app.run(debug=True)
