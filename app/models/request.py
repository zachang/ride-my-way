from app import db
from datetime import datetime
from app.models.base import Base

class Request(Base):
    """Define fields for Request."""

    __tablename__ = "request"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rideId = db.Column(db.Integer, db.ForeignKey('ride.id'), nullable=False)
    status = db.Column(db.String(10), server_default='pending', nullable=True)


    def __init__(self, **kwargs):
        """initialize class."""
        self.userId = kwargs['userId']
        self.rideId = kwargs['rideId']


    def __repr__(self):
        return "<Request: {}>".format(self.__tablename__)