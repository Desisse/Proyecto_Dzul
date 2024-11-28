import unittest
from unittest.mock import MagicMock, Mock, patch
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from api.controllers import Users, Events, Reservations 
from api.models import UserModel, db
from src.app import app, db
import json
from src.main import EventReservationSystem

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    api = Api(app)
    db.init_app(app)

    api.add_resource(Users, "/api/users")             # CRUD para usuarios
    api.add_resource(Events, "/api/events")           # CRUD para eventos
    api.add_resource(Reservations, "/api/reservations")  # CRUD para reservas
    

    with app.app_context():
        db.create_all()
    
    yield app.test_client()


# def test_get_users(app):
#     response = app.get('/api/users')
#     assert response.status_code == 200
#     assert response.json == []

def test_post_user(app):
    response = app.post('/api/users', json={
    'username': 'TESTING',
    'email': 'testing@example.com',
    'password': 'prueba123'
})
    assert response.status_code == 201

    # with app.application.app_context():
    #     user = UserModel.query.filter_by(email='john@example.com').first()
    #     assert user is not None
    #     assert user.username == 'John Doe'