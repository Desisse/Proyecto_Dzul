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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
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

    with app.app_context():
        db.session.remove()
        db.drop_all()

# def test_get_users(app):
#     response = app.get('/api/users')
#     assert response.status_code == 200
#     assert response.json == []

def test_post_user(app):
    response = app.post('/api/users', json={
    'username': 'John Doe',
    'email': 'john@example.com',
    'password': 'securepassword123'
})
    assert response.status_code == 201
    assert response.json == {'id': 1, 'username': 'John Doe', 'email': 'john@example.com', 'password': 'securepassword123'}