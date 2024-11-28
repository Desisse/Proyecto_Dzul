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
    # Relación con Pagos 
    payments = db.relationship('PaymentModel', backref='payer', lazy=True)
    
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
        return f"Event(name={self.name}, date={self.date}, capacity={self.max_capacity})"

# Modelo de Reserva
class ReservationModel(db.Model):
    __tablename__ = 'reservations'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    reservation_date = db.Column(db.DateTime, nullable=False)
    discount = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"Reservation(user_id={self.user_id}, event_id={self.event_id}, date={self.reservation_date}, discount={self.discount})"

# Modelo de Pago
class PaymentModel(db.Model):
    __tablename__ = 'payments' 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    reservation_id = db.Column(db.Integer, db.ForeignKey('reservations.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    
    # Relación con Usuario
    user = db.relationship('UserModel', backref='payer', lazy=True)
    # Relación con Reserva
    reservation = db.relationship('ReservationModel', backref='payments', lazy=True)

    def __repr__(self):
        return f"Payment (user_id = {self.user_id}, reservation_id = {self.reservation_id}, amount = {self.amount}, payment_date = {self.payment_date}, payment_method = {self.payment_method})"

