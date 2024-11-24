from .extensions import db

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

#Model de Evento
class EventModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    
    # Relación con Reservas
    reservations = db.relationship('ReservationModel', backref='event', lazy=True)
    
    def __repr__(self):
        return f"Event (name = {self.name}, date = {self.date}, capacity = {self.max_capacity})"
    
#Model de Reserva
class ReservationModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event_model.id'), nullable=False)
    reservation_date = db.Column(db.DateTime, nullable=False)
    discount = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"Reservation (user_id = {self.user_id}, event_id = {self.event_id}, date = {self.reservation_date}, discount = {self.discount})"