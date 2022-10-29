from flask_marshmallow import Marshmallow

from ..models.users import UserModel

ma = Marshmallow()


class UserSChema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

        fields = ("username", "public_id", "password", "email", 'admin')


user_schemas = UserSChema()
users_schemas = UserSChema(many=True)
