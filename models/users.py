from ..slq_alchemy import db


class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    admin = db.Column(db.Boolean, default=False)


class AnimaisModel(db.Model):
    __tablename__ = "animal"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    raca = db.Column(db.String)  # raça
    animal_id = db.Column(
        db.Integer, db.ForeignKey("user.id"),  nullable=False)
    user = db.relationship("UserModel", backref="pets")

    def __init__(self, name, raca, user):
        self.name = name
        self.raca = raca
        self.user = user
