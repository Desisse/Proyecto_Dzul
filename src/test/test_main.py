from datetime import datetime
import unittest
from unittest.mock import MagicMock, Mock, patch
import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from api.controllers import Payment, Payments, Reservation, User, Users, Events, Event, Reservations 
from api.models import PaymentModel, UserModel, db
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

    api.add_resource(Users, "/api/users")             
    api.add_resource(User, "/api/users/<int:user_id>")  
    api.add_resource(Events, "/api/events")  
    api.add_resource(Event,"/api/events/<int:event_id>")         
    api.add_resource(Reservations, "/api/reservations")
    api.add_resource(Reservation, "/api/reservations/<int:reservation_id>")
    api.add_resource(Payments, "/api/payments")
    api.add_resource(Payment, "/api/payments/<int:payment_id>")  
    

    with app.app_context():
        db.create_all()
    
    yield app.test_client()

#PRUEBAS USERS

def test_post_user(app):
    response = app.post('/api/users', json={
    'username': 'TESTING',
    'email': 'testing@example.com',
    'password': 'prueba123'
})
    assert response.status_code == 201

def test_create_user_with_empty_username(app):
    response = app.post('/api/users', json={
        'username': '',
        'email': 'testing@example.com',
        'password': 'XXXXXXXXX'
    })
    assert response.status_code == 409
    assert 'Username cannot be empty' in response.get_json('message', '')


def test_create_user_with_empty_password(app):
    response = app.post('/api/users', json={
        'username': 'XXXXXXX',
        'email': 'pruebag@example.com',
        'password': ''
    })
    print(response.get_json())
    assert response.status_code == 400
    assert 'Password cannot be empty' in response.get_json('message', '')

def test_create_user_with_existing_username(app):
    response = app.post('/api/users', json={
        'username': 'TEST',
        'email': 'testing@example.com',
        'password': 'XXXXXXXXX'
    })
    print(response.get_json())
    assert response.status_code == 409
    assert 'Username already exists' in response.get_json()['error']

def test_create_user_with_existing_email(app):
    response = app.post('/api/users', json={
        'username': 'XXXXXXX',
        'email': 'testing@example.com',
        'password': 'XXXXXXXXX'
    })
    print(response.get_json())  
    assert response.status_code == 409
    assert 'email already exists' in response.get_json().get('error', '')


def test_create_user_with_invalid_email(app):
    response = app.post('/api/users', json={
        'username': 'XXXXXXX',
        'email': 'invalid_email',
        'password': 'XXXXXXXXX'
    })
    print(response.get_json()) 
    assert response.status_code == 400
    assert 'Invalid email format' in response.get_json().get('error', '')

def test_get_user(app):
    response = app.get('/api/users')
    assert response.status_code == 200
    data = response.get_json()
    print("Lista de usuarios:", data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_user_by_id(app):
    response = app.get('/api/users/3')
    assert response.status_code == 200
    data = response.get_json()
    print("Usuario:", data)
    assert isinstance(data, dict)
    assert 'id' in data
    assert 'username' in data
    assert 'email' in data

def test_get_user_by_id_not_found(app):
    response = app.get('/api/users/999')
    assert response.status_code == 404
    data = response.get_json()
    print("Usuario no encontrado:", data)
    assert 'error' in data
    assert 'User not found' in data['error']

def test_create_user_with_a_reservation(app):
    response = app.post('/api/users', json={
        'username': 'XXXXXXX',
        'email': 'testing@example.com',
        'password': 'XXXXXXXXX',
        'reservation_id': 1
    })
    assert response.status_code == 201
    data = response.get_json()
    print("Usuario creado con reserva:", data)
    assert 'id' in data
    assert 'username' in data
    assert 'email' in data
    assert 'reservation_id' in data     

#PRUEBAS EVENTOS
def test_post_event(app):
    date_string = '2024-12-14T00:00:00'

    response = app.post('/api/events', json={
    'name': 'POSADA',
    'date': date_string,
    'max_capacity': 50
})
    assert response.status_code == 201

def test_post_event_negative_capacity(app):
    date_string = '2024-12-14T00:00:00'

    response = app.post('/api/events', json={
    'name': 'POSADA',
    'date': date_string,
    'max_capacity': -50
})
    assert response.status_code == 400
    assert 'Max capacity must be greater than 0' in response.get_json().get('error', '')

def test_post_event_invalid_date(app):
    date_wrong = '12daff'
    response = app.post('/api/events', json={
        'name': 'Evento Test',
        'date': date_wrong,
        'max_capacity': 50
    })
    data = response.get_json()
    print("respuesta:", data)
    assert response.status_code == 400
    assert response.json['message'] == 'La fecha proporcionada no es válida'

def test_post_event_duplicate(app):
    date_string = '2024-12-14T00:00:00'
    response = app.post('/api/events', json={
     'name': 'POSADA',
     'date': date_string,
     'max_capacity': 50
     })
    data = response.get_json()
    print("Evento duplicado:", data)
    assert response.status_code == 400
    assert response.json['message'] == 'Ya existe un evento con el mismo nombre y fecha'

def test_get_event(app):
    response = app.get('/api/events')
    assert response.status_code == 200
    data = response.get_json()
    print("Lista de eventos:", data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_event_by_id(app):
    response = app.get('/api/events/2')
    assert response.status_code == 200
    data = response.get_json()
    print("Evento:", data)
    assert isinstance(data, dict)
    assert 'id' in data
    assert 'name' in data
    assert 'date' in data
    assert 'max_capacity' in data

def test_delete_event(app):
    # Verificar si el evento existe antes de la eliminación
    response = app.get('/api/events/3')
    assert response.status_code == 200  
    data = response.get_json()
    print("Evento antes de eliminar:", data)

    # Eliminar el evento
    response = app.delete('/api/events/3')
    assert response.status_code == 204  

    # Verificar que el evento ya no exista
    response = app.get('/api/events/3')
    assert response.status_code == 404  
    data = response.get_json()
    print("Evento Eliminado:", data) 


#PRUEBAS RESERVAS

def test_post_reservation(app):
    response = app.post('/api/reservations', json={
        'user_id': 3,
        'event_id': 2,
        'reservation_date': '2024-12-14T00:00:00',
        'discount': 10.0
    })
    assert response.status_code == 201
    data = response.get_json()
    print("Reserva:", data) 

def test_reservation_for_nonexistent_event(app):
    response = app.post('/api/reservations', json={
        'user_id': 1,
        'event_id': 3,
        'reservation_date': '2024-12-14T00:00:00',
        'discount': 0.0
    })
    assert response.status_code == 404
    assert response.json['message'] == 'No se puede reservar'

def test_reservation_for_nonexistent_user(app):
    response = app.post('/api/reservations', json={
        'user_id': 4,
        'event_id': 2,
        'reservation_date': '2024-12-14T00:00:00',
        'discount': 0.0
    })
    assert response.status_code == 404
    assert response.json['message'] == 'No se puede reservar'

def test_duplicate_reservation(app):
    response = app.post('/api/reservations', json={
        'user_id': 1,
        'event_id': 2,
        'reservation_date': '2024-12-14T00:00:00',
        'discount': 0.0
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Ya existe una reserva para este usuario y evento'

def test_get_reservation(app):
    response = app.get('/api/reservations')
    assert response.status_code == 200
    data = response.get_json()
    print("Lista de reservas:", data)
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_reservation_by_id(app):
    response = app.get('/api/reservations/1')
    assert response.status_code == 200
    data = response.get_json()
    print("Reserva:", data)
    assert isinstance(data, dict)
    assert 'id' in data
    assert 'user_id' in data
    assert 'event_id' in data
    assert 'reservation_date' in data
    assert 'discount' in data

def test_delete_reservation(app):
    response = app.get('/api/reservations/1')
    assert response.status_code == 200
    data = response.get_json()
    print("Reserva antes de eliminar:", data)
    response = app.delete('/api/reservations/1')
    assert response.status_code == 204
    response = app.get('/api/reservations/1')
    assert response.status_code == 404
    data = response.get_json()
    print("Reserva Eliminada:", data)

#PRUEBAS PAGOS
def test_create_payment_valid(app):
    response = app.post('/api/payments', json={
        'user_id': 3,
        'reservation_id': 2,
        'amount': 1000.0,
        'payment_date': '2024-12-14T00:00:00',
        'payment_method': 'Tarjeta de crédito'
    })
    assert response.status_code == 201
    data = response.get_json()
    print("Pago aprobado:", data)

def test_payment_for_nonexistent_reservation(app):
    response = app.post('/api/payments', json={
        'user_id': 3,
        'reservation_id': 3,
        'amount': 1000.0,
        'payment_date': '2024-12-14T00:00:00',
        'payment_method': 'Tarjeta de crédito'
    })
    assert response.status_code == 404
    assert response.json['message'] == ''

def test_payment_with_discount(app):
    response = app.post('/api/payments', json={
        'user_id': 3,
        'reservation_id': 2,
        'amount': 950.0,
        'payment_date': '2024-12-14T00:00:00',
        'payment_method': 'Tarjeta de crédito'
    })
    assert response.status_code == 201
    data = response.get_json()
    print("Pago con descuento:", data)

def test_payment_for_nonexistent_user(app):
    response = app.post('/api/payments', json={
        'user_id': 4,
        'reservation_id': 2,
        'amount': 1000.0,
        'payment_date': '2024-12-14T00:00:00',
        'payment_method': 'Tarjeta de crédito'
    })
    assert response.status_code == 404
    assert response.json['message'] == ''

def test_get_payments(app):
    response = app.get('/api/payments')
    assert response.status_code == 200
    data = response.get_json()
    print("Lista de pagos:", data)
    assert isinstance(data, list)
    assert len(data) > 0