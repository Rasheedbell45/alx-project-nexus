from flask_restx import Namespace, Resource, fields
from flask import request
from ..extensions import db
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_ns = Namespace("auth", description="Authentication operations")

signup_model = auth_ns.model("Signup", {
    "username": fields.String(required=True),
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})

login_model = auth_ns.model("Login", {
    "username": fields.String(required=True),
    "password": fields.String(required=True),
})

@auth_ns.route("/register")
class Register(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()
        if User.query.filter((User.username == data['username']) | (User.email == data['email'])).first():
            return {"message": "Username or email already exists"}, 400
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password'])
        )
        db.session.add(user)
        db.session.commit()
        return {"message": "User created"}, 201

@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password_hash, data['password']):
            return {"message": "Invalid credentials"}, 401
        token = create_access_token(identity=user.id)
        return {"access_token": token}, 200
