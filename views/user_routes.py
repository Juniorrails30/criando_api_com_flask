import uuid

from flask import Blueprint, request
from werkzeug.security import generate_password_hash

from ..checa_email import check
from ..models.users import UserModel
from ..schema.userschema import user_schemas, users_schemas
from ..slq_alchemy import db

bp_user = Blueprint("User", __name__)


@bp_user.route("/users", methods=["GET"])
def get_users():
    all_users = UserModel.query.all()
    resultado = users_schemas.dump(all_users)
    return users_schemas.jsonify(resultado)


@bp_user.route("/users/<public_id>", methods=["GET"])
def get_user(public_id):
    user = UserModel.query.filter_by(public_id=public_id)
    resultado = users_schemas.dump(user)
    return users_schemas.jsonify(resultado)


@bp_user.route("/users", methods=["POST"])
def post_user():
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    checa = check(email)
    hash_password = generate_password_hash(password)
    if checa is True:
        new_user = UserModel(username=username, password=hash_password,
                             public_id=str(uuid.uuid4()),
                             email=email, admin=False)
        db.session.add(new_user)
        db.session.commit()
        resultado = user_schemas.dump(new_user)
        return user_schemas.jsonify(resultado)
    return checa


@bp_user.route("/users/<public_id>", methods=["PUT"])
def put_user(public_id):
    user = UserModel.query.filter_by(public_id=public_id)
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    checa = check(email)
    hash_password = generate_password_hash(password)
    user.username = username
    user.password = hash_password
    user.email = email
    if checa is True:
        user_alterado = UserModel(username=username, password=hash_password,
                                  public_id=str(uuid.uuid4()),
                                  email=email, admin=False)
        db.session.add(user_alterado)
        db.session.commit()
        resultado = user_schemas.dump(user_alterado)
        return user_schemas.jsonify(resultado)
    return checa
