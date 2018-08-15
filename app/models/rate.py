from app import db
from datetime import datetime
from app.models.base import Base

class Rate(Base):
    """Define fields for Rate."""

    __tablename__ = "rate"

    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    ride_id = db.Column(db.String, db.ForeignKey('ride.id'), nullable=False)
    rate_status = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, **kwargs):
        """initialize class."""
        self.user_id = kwargs['user_id']
        self.ride_id = kwargs['ride_id']


    def __repr__(self):
        return "<Rate: {}>".format(self.__tablename__)