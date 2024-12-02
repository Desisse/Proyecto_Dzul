from datetime import datetime
from flask import Flask, Response, json
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from api.models import EventModel, ReservationModel, UserModel, PaymentModel, db
import re

def validate_email_format(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w{2,4}$'
    if not re.match(email_regex, email):
        abort(400, message="Formato inválido para el email.")

def check_user_exists(username, email):
    if UserModel.query.filter_by(username=username).first():
        abort(409, message="El nombre de usuario ya existe.")
    if UserModel.query.filter_by(email=email).first():
        abort(409, message="El email ya existe.")

def check_event_capacity(event_id):
    event = EventModel.query.filter_by(id=event_id).first()
    if not event:
        abort(404, message="Evento no encontrado.")
    reservations_count = ReservationModel.query.filter_by(event_id=event_id).count()
    if reservations_count >= event.max_capacity:
        abort(400, message="El evento ha alcanzado su capacidad máxima.")

def check_reservation_exists(user_id, event_id):
    if ReservationModel.query.filter_by(user_id=user_id, event_id=event_id).first():
        abort(409, message="El usuario ya tiene una reserva para este evento.")

def validate_password(password):
    if not password:
        abort(400, message="La contraseña es requerida.")
    if len(password) < 8:
        abort(400, message="La contraseña debe tener al menos 8 caracteres.")

def check_event_negative_capacity(max_capacity):
    if max_capacity <= 0:
        abort(400, message="La capacidad del evento debe ser un número positivo.")

def is_valid_date(date_str):
    date_format = "%Y-%m-%dT%H:%M:%S"
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

# Parsers para validación
user_args = reqparse.RequestParser()
user_args.add_argument("username", type=str, help="El usuario es requerido.", required=True)
user_args.add_argument("email", type=str, help="El email es requerido.", required=True)
user_args.add_argument('password', type=str, required=True, help="La contraseña es requerida.")

event_args = reqparse.RequestParser()
event_args.add_argument("name", type=str, help="El nombre del evento es requerido", required=True)
event_args.add_argument("date", type=str, help="La fecha del evento es requerida.", required=True)
event_args.add_argument("max_capacity", type=int, help="La capacidad del evento es requerida.", required=True)

reservation_args = reqparse.RequestParser()
reservation_args.add_argument("user_id", type=int, help="El ID del usuario es requerido.", required=True)
reservation_args.add_argument("event_id", type=int, help="El ID del evento es requerido.", required=True)
reservation_args.add_argument("reservation_date", type=str, help="La fecha de reservacion es requerida.", required=True)
reservation_args.add_argument("discount", type=float, help="Descuento opcional.", required=False)

payment_args = reqparse.RequestParser()
payment_args.add_argument("user_id", type=int, help="El ID del usuario es requerido.", required=True)
payment_args.add_argument("reservation_id", type=int, help="El ID de la reserva es requerido.", required=True)
payment_args.add_argument("amount", type=float, help="El monto del pago es requerido.", required=True)
payment_args.add_argument("payment_date", type=str, help="La fecha del pago es requerida.", required=True)
payment_args.add_argument("payment_method", type=str, help="El método de pago es requerido.", required=True)

user_fields = {
    "id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "password": fields.String
}

event_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "date": fields.DateTime,
    "max_capacity": fields.Integer
}

reservation_fields = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "event_id": fields.Integer,
    "reservation_date": fields.DateTime,
    "discount": fields.Float
}

payment_fields = {
    "id": fields.Integer,
    "user_id": fields.Integer,
    "reservation_id": fields.Integer,
    "amount": fields.Float,
    "payment_date": fields.DateTime,
    "payment_method": fields.String
}

# Recursos de API
class Users(Resource):
    @marshal_with(user_fields)
    def post(self):
        args = user_args.parse_args()
        validate_email_format(args["email"])
        check_user_exists(args["username"], args["email"])
        validate_password(args["password"])
        user = UserModel(username=args["username"], email=args["email"], password=args["password"])
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(user_fields)
    def get(self):
        users = UserModel.query.all()
        if not users:
            abort(404, message="No users found")
        return users

class User(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User not found")
        return user

    def delete(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            abort(404, message="User not found")
        db.session.delete(user)
        db.session.commit()
        return Response(status=204)

class Events(Resource):
    @marshal_with(event_fields)
    def post(self):
        args = event_args.parse_args()
        check_event_negative_capacity(args["max_capacity"])
        if not is_valid_date(args["date"]):
            abort(400, message="La fecha proporcionada no es válida")

        event_date = datetime.strptime(args["date"], "%Y-%m-%dT%H:%M:%S")
        existing_event = EventModel.query.filter_by(name=args["name"], date=event_date).first()
        if existing_event:
            abort(400, message="Ya existe un evento con el mismo nombre y fecha")
        event = EventModel(name=args["name"], date=datetime.strptime(args["date"], "%Y-%m-%dT%H:%M:%S"), max_capacity=args["max_capacity"])
        db.session.add(event)
        db.session.commit()
        return event, 201

    @marshal_with(event_fields)
    def get(self):
        events = EventModel.query.all()
        if not events:
            abort(404, message="No events found")
        return events

class Event(Resource):
    @marshal_with(event_fields)
    def get(self, event_id):
        event = EventModel.query.filter_by(id=event_id).first()
        if not event:
            abort(404, message="Event not found")
        return event

    def delete(self, event_id):
        event = EventModel.query.get(event_id)
        if not event:
            abort(404, message="Event not found")
        db.session.delete(event)
        db.session.commit()
        return '', 204 

class Reservations(Resource):
    @marshal_with(reservation_fields)
    def post(self):
        args = reservation_args.parse_args()
        try:
            reservation_date = datetime.fromisoformat(args["reservation_date"])
        except ValueError:
            abort(400, message="Invalid date format. Use (YYYY-MM-DDTHH:MM:SS).")
        
        user = db.session.get(UserModel, args["user_id"])
        if not user:
            abort(404, message="Usuario no encontrado.")
        
        event = db.session.get(EventModel, args["event_id"])
        if not event:
            abort(404, message="Evento no encontrado.")
        
        existing_reservation = ReservationModel.query.filter_by(
        user_id=args["user_id"], event_id=args["event_id"]
        ).first()
        if existing_reservation:
            abort(400, message="El usuario ya tiene una reserva para este evento.")

        check_event_capacity(args["event_id"])
        reservation = ReservationModel(
            user_id=args["user_id"],
            event_id=args["event_id"],
            reservation_date=reservation_date,
            discount=args.get("discount")
        )
        db.session.add(reservation)
        db.session.commit()
        return reservation, 201

    @marshal_with(reservation_fields)
    def get(self):
        reservations = ReservationModel.query.all()
        if not reservations:
            abort(404, message="No reservations found")
        return reservations

class Reservation(Resource):
    @marshal_with(reservation_fields)
    def get(self, reservation_id):
        reservation = ReservationModel.query.filter_by(id=reservation_id).first()
        if not reservation:
            abort(404, message="Reservation not found")
        return reservation

    def delete(self, reservation_id):
        reservation = ReservationModel.query.get(reservation_id)
        if not reservation:
            abort(404, message="Reservation not found")
        db.session.delete(reservation)
        db.session.commit()
        return '', 204

class Payments(Resource):
    @marshal_with(payment_fields)
    def post(self):
        args = payment_args.parse_args()
        try:
            payment_date = datetime.fromisoformat(args["payment_date"])
        except ValueError:
            abort(400, message="Invalid date format. Use (YYYY-MM-DDTHH:MM:SS).")

        user = db.session.get(UserModel, args["user_id"])
        if not user:
            abort(404, message="Usuario no encontrado.")

        reservation = db.session.get(ReservationModel, args["reservation_id"])
        if not reservation:
            abort(404, message="Reserva no encontrada.")

        payment = PaymentModel(
            user_id=args["user_id"],
            reservation_id=args["reservation_id"],
            amount=args["amount"],
            payment_date=payment_date,
            payment_method=args["payment_method"]
        )
        db.session.add(payment)
        db.session.commit()
        return payment, 201

    @marshal_with(payment_fields)
    def get(self):
        payments = PaymentModel.query.all()
        if not payments:
            abort(404, message="No payments found")
        return payments

class Payment(Resource):
    @marshal_with(payment_fields)
    def get(self, payment_id):
        payment = PaymentModel.query.filter_by(id=payment_id).first()
        if not payment:
            abort(404, message="Payment not found")
        return payment

    def delete(self, payment_id):
        payment = PaymentModel.query.get(payment_id)
        if not payment:
            abort(404, message="Payment not found")
        db.session.delete(payment)
        db.session.commit()
        return '', 204