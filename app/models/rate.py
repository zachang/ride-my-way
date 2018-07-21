from app import db
from datetime import datetime
from app.models.base import Base

class Rate(Base):
    """Define fields for Ride."""

    __tablename__ = "rate"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rideId = db.Column(db.Integer, db.ForeignKey('ride.id'), nullable=False)
    rateStatus = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, **kwargs):
        """initialize class."""
        self.userId = kwargs['userId']
        self.rideId = kwargs['rideId']


    def __repr__(self):
        return "<Rate: {}>".format(self.__tablename__)