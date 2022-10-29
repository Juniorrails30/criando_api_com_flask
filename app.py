from flask import Flask


def create_app():
    app = Flask(__name__)
    from .slq_alchemy import db
    from .views.user_routes import bp_user
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///banco.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.register_blueprint(bp_user)
    db.init_app(app)

    @app.before_first_request
    def create_table():
        db.create_all()

    return app
