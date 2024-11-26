from flask import Flask
from flask_restful import Api
from api.extensions import db
from api.controllers import Users, Events, Reservations

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

with app.app_context():
    db.init_app(app)
    db.create_all()

# Rutas de las APIs
api.add_resource(Users, "/api/users")             # CRUD para usuarios
api.add_resource(Events, "/api/events")           # CRUD para eventos
api.add_resource(Reservations, "/api/reservations")  # CRUD para reservas

if __name__ == '__main__':
    app.run(debug=True)