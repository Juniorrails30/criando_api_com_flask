from flask_marshmallow import Marshmallow

from ..models.users import AnimaisModel, UserModel

ma = Marshmallow()


class UserSChema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    public_id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    pets = ma.auto_field()
    admin = ma.auto_field()
    password = ma.auto_field()


user_schemas = UserSChema()
users_schemas = UserSChema(many=True)


class AnimalSchema(ma.SQLAlchemySchema):

    class Meta:
        model = AnimaisModel

    name = ma.auto_field()
    raca = ma.auto_field()
    user = ma.auto_field()
    animal_id = ma.auto_field()


animal_schemas = AnimalSchema()
animais_schemas = AnimalSchema(many=True)
