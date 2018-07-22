from app import db
from datetime import datetime
from app.models.base import Base
from app.models.rate import Rate


class Ride(Base):
    """Define fields for Ride."""

    __tablename__ = "ride"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    carName = db.Column(db.String(100), nullable=True)
    departureTime = db.Column(db.String(250), nullable=False)
    seatCount = db.Column(db.Integer, nullable=False)
    seatTaken = db.Column(db.Integer, default=0, nullable=False)
    available = db.Column(db.Boolean, default=False, nullable=True)
    rates = db.relationship('Rate', backref='ride', lazy=True)


    def __init__(self, **kwargs):
        """initialize class."""
        self.userId = kwargs['userId']
        self.departureTime = kwargs['departureTime']
        self.seatCount = kwargs['seatCount']


    def __repr__(self):
        return "<Ride: {}>".format(self.__tablename__)