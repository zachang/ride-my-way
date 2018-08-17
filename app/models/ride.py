from app import db
from datetime import datetime
from app.models.base import Base
from app.models.rate import Rate


class Ride(Base):
    """Define fields for Ride."""

    __tablename__ = "ride"

    user_id = db.Column(db.String, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    car_name = db.Column(db.String(100), nullable=True)
    departure_time = db.Column(db.String(250), nullable=False)
    seat_count = db.Column(db.Integer, nullable=False)
    seat_taken = db.Column(db.Integer, default=0, nullable=False)
    available = db.Column(db.Boolean, default=False, nullable=True)
    rates = db.relationship('Rate', backref='ride', lazy=True)


    def __init__(self, **kwargs):
        """initialize class."""
        self.user_d = kwargs['user_d']
        self.departure_time = kwargs['departure_time']
        self.seat_count = kwargs['seat_count']


    def __repr__(self):
        return "<Ride: {}>".format(self.__tablename__)