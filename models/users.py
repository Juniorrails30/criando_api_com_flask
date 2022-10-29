from enum import unique

from ..slq_alchemy import db


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, public_id, email, password, admin):
        self.username = username
        self.public_id = public_id
        self.email = email
        self.password = password
        self.admin = admin
