from typing import List
from datetime import datetime
from flask import app
from api.models import UserModel, EventModel, ReservationModel, db


class EventReservationSystem:
    def __init__(self):
        self.context_initialized = False

    def initialize_context(self):
        if not self.context_initialized:
            with app.app_context():
                db.create_all()
            self.context_initialized = True

    def add_user(self, username: str, email: str):
        username = username.strip()
        email = email.strip()
        print(f"Intentando agregar usuario: {username}, {email}")
        with app.app_context():
            if UserModel.query.filter_by(username=username).first():
                print(f"El usuario '{username}' ya existe.")
                return
            if UserModel.query.filter_by(email=email).first():
                print(f"El email '{email}' ya está registrado.")
                return
            user = UserModel(username=username, email=email)
            db.session.add(user)
            db.session.commit()
            print(f"Usuario agregado: {username}")

    def add_event(self, name: str, date: str, max_capacity: int):
        name = name.strip()
        print(f"Intentando agregar evento: {name}, {date}, capacidad máxima: {max_capacity}")
        with app.app_context():
            event_date = datetime.strptime(date, "%Y-%m-%d")
            event = EventModel(name=name, date=event_date, max_capacity=max_capacity)
            db.session.add(event)
            db.session.commit()
            print(f"Evento agregado: {name}")

    def add_reservation(self, user_id: int, event_id: int, reservation_date: str, discount: float = 0.0):
        print(f"Intentando agregar reserva: usuario_id={user_id}, evento_id={event_id}, fecha={reservation_date}, descuento={discount}")
        with app.app_context():
            event = EventModel.query.get(event_id)
            if not event:
                print("El evento no existe.")
                return
            if ReservationModel.query.filter_by(user_id=user_id, event_id=event_id).first():
                print("El usuario ya tiene una reserva para este evento.")
                return
            reservations_count = ReservationModel.query.filter_by(event_id=event_id).count()
            if reservations_count >= event.max_capacity:
                print("El evento ha alcanzado su capacidad máxima.")
                return
            reservation = ReservationModel(
                user_id=user_id,
                event_id=event_id,
                reservation_date=datetime.strptime(reservation_date, "%Y-%m-%d"),
                discount=discount
            )
            db.session.add(reservation)
            db.session.commit()
            print("Reserva agregada con éxito.")

    def list_users(self):
        with app.app_context():
            users = UserModel.query.all()
            print("Usuarios registrados:")
            for user in users:
                print(f"- {user.id}: {user.username} ({user.email})")

    def list_events(self):
        with app.app_context():
            events = EventModel.query.all()
            print("Eventos registrados:")
            for event in events:
                print(f"- {event.id}: {event.name} (Fecha: {event.date}, Capacidad: {event.max_capacity})")

    def list_reservations(self):
        with app.app_context():
            reservations = ReservationModel.query.all()
            print("Reservas realizadas:")
            for reservation in reservations:
                print(f"- Usuario {reservation.user_id} reservado para evento {reservation.event_id} el {reservation.reservation_date} (Descuento: {reservation.discount})")

# Ejemplo de uso
if __name__ == "__main__":
    system = EventReservationSystem()
    system.initialize_context()

    # Agregar usuarios
    system.add_user("usuario1", "usuario1@example.com")
    system.add_user("usuario2", "usuario2@example.com")

    # Agregar eventos
    system.add_event("Concierto Rock", "2024-12-01", 100)
    system.add_event("Conferencia Tech", "2024-12-15", 50)

    # Listar usuarios y eventos
    system.list_users()
    system.list_events()

    # Agregar reservas
    system.add_reservation(1, 1, "2024-12-01")
    system.add_reservation(2, 1, "2024-12-01", discount=0.1)

    # Listar reservas
    system.list_reservations()
