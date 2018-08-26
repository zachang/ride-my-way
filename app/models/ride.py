from app import db
from datetime import datetime
from app.models.base import Base
from app.models.rate import Rate


class Ride(Base):
    """Define fields for Ride."""

    __tablename__ = "ride"

    user_id = db.Column(db.String, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    car_name = db.Column(db.String(100), nullable=True)
    start_pos = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.DateTime)
    seat_count = db.Column(db.Integer, nullable=False)
    seat_taken = db.Column(db.Integer, default=0, nullable=False)
    available = db.Column(db.Boolean, default=False, nullable=False)
    completed = db.Column(db.String(10), default='no', nullable=False)
    rates = db.relationship('Rate', backref='ride', lazy=True)


    def __init__(self, **kwargs):
        """initialize class."""
        self.departure_time = kwargs['departure_time']
        self.seat_count = kwargs['seat_count']
        self.car_name = kwargs['car_name']
        self.start_pos = kwargs['start_pos']
        self.destination = kwargs['destination']

    def __repr__(self):
        return "<Ride: {}>".format(self.__tablename__)