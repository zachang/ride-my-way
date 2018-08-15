from app import db
from datetime import datetime
from app.models.base import Base

class Request(Base):
    """Define fields for Request."""

    __tablename__ = "request"

    userId = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    rideId = db.Column(db.String, db.ForeignKey('ride.id'), nullable=False)
    status = db.Column(db.String(10), server_default='pending', nullable=True)


    def __init__(self, **kwargs):
        """initialize class."""
        self.user_id = kwargs['user_id']
        self.ride_id = kwargs['ride_id']


    def __repr__(self):
        return "<Request: {}>".format(self.__tablename__)