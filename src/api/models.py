from .extensions import db

# Modelo de Usuario
class UserModel(db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    
    # Relación con Reservas
    reservations = db.relationship('ReservationModel', backref='user', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

# Modelo de Evento
class EventModel(db.Model):
    __tablename__ = 'events' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    
    # Relación con Reservas
    reservations = db.relationship('ReservationModel', backref='event', lazy=True)
    
    def __repr__(self):
        return f"Event (name = {self.name}, date = {self.date}, capacity = {self.max_capacity})"

# Modelo de Reserva
class ReservationModel(db.Model):
    __tablename__ = 'reservations' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False) 
    reservation_date = db.Column(db.DateTime, nullable=False)
    discount = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"Reservation (user_id = {self.user_id}, event_id = {self.event_id}, date = {self.reservation_date}, discount = {self.discount})"
