from app import db
from datetime import datetime
from app.models.base import Base

class Request(Base):
    """Define fields for Request."""

    __tablename__ = "request"

    user_id = db.Column(db.String, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=False)
    ride_id = db.Column(db.String, db.ForeignKey('ride.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(10), server_default='pending', nullable=True)
    completed = db.Column(db.String(10), server_default='no', nullable=False)


    def __init__(self, **kwargs):
        """initialize class."""
        self.user_id = kwargs['user_id']
        self.ride_id = kwargs['ride_id']


    def __repr__(self):
        return "<Request: {}>".format(self.__tablename__)
