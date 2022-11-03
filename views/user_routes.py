import datetime
from functools import wraps
from uuid import uuid4

import jwt
from flask import Blueprint, current_app, jsonify, make_response, request
from werkzeug.security import check_password_hash, generate_password_hash

from ..checa_email import check
from ..models.users import UserModel
from ..schema.userschema import user_schemas, users_schemas
from ..slq_alchemy import db

bp_user = Blueprint("User", __name__)


def token_required(f):
    @wraps(f)
    def decorete(*args, **kwargs):
        token = None
        if "x-access-token" in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({"message": "token is missing!"}), 401

        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms="HS256")
            current_user = UserModel.query.filter_by(
                public_id=data["public_id"]).first()
        except ValueError:
            return jsonify({"message": "token in valid!"}), 401
        return f(current_user, *args, **kwargs)
    return decorete


@bp_user.route("/users", methods=["GET"])
# @token_required
def get_users():
    # if current_user.admin:
    #     return {"message": "Acesso negado!"}
    all_users = UserModel.query.all()
    resultado = users_schemas.dump(all_users)
    return (resultado)


@bp_user.route("/users/<public_id>", methods=["GET"])
def get_user(public_id):
    user = UserModel.query.filter_by(public_id=public_id)
    resultado = users_schemas.dump(user)
    return (resultado)


@bp_user.route("/users", methods=["POST"])
def post_user():
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    checa = check(email)
    hash_password = generate_password_hash(password)
    if checa is True:
        new_user = UserModel(username=username, password=hash_password,
                             public_id=str(uuid4()),
                             email=email, admin=False)
        db.session.add(new_user)
        db.session.commit()
        resultado = user_schemas.dump(new_user)
        return user_schemas.jsonify(resultado)
    return checa


@bp_user.route("/users/<public_id>", methods=["PUT"])
def put_user(public_id):
    # if not current_user.admin:
    #     return jsonify({"message": "token in valid!"}), 401
    user = UserModel.query.filter_by(public_id=public_id).first()
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    hash_password = generate_password_hash(password)
    checa = check(email)
    user.username = username
    user.password = hash_password
    user.email = email
    if checa is True:
        user_alerado = UserModel(username=username, password=hash_password,
                                 email=email,
                                 public_id=str(uuid4()), admin=False)
        db.session.commit()
        result = user_schemas.dump(user_alerado)
        return user_schemas.jsonify(result)
    return checa


@bp_user.route("/login")
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response({"message": "erro"}), 401
    user = UserModel.query.filter_by(username=auth.username).first()

    if not user:
        return make_response({"message": "erro"}), 401

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({"public_id": user.public_id,
                            'exp': datetime.datetime.utcnow()
                            + datetime.timedelta(minutes=30)},
                           current_app.config["SECRET_KEY"])

        return jsonify({"token": token})
    return {"message": "login ou senha estão errados!"}
