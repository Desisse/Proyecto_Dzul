from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from api.extensions import db
from api.controllers import User, Users


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
api = Api(app)

with app.app_context():
    db.init_app(app)
    db.create_all()

api.add_resource(Users, "/api/users")
api.add_resource(User, "/api/user/<int:user_id>")


if __name__ == '__main__':
    app.run(debug=True)

    