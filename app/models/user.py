from app import db
from app.models.base import Base
from app.models.ride import Ride
from app.models.rate import Rate


class User(Base):
    """Define fields for User."""

    __tablename__ = "user"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    firstName = db.Column(db.String(250), nullable=False)
    lastName = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False)
    phoneNo = db.Column(db.String(50), unique=True , nullable=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=True, nullable=False)
    userImage = db.Column(db.String(200), nullable=True)
    isSocial = db.Column(db.Boolean, default=False, nullable=True)
    regType = db.Column(db.String(50), default='regular', nullable=True)
    rides = db.relationship('Ride', backref='user', lazy=True)
    rates = db.relationship('Rate', backref='user', lazy=True)


    def __init__(self, **kwargs):
        """initialize class."""
        self.firstName = kwargs['firstName']
        self.lastName = kwargs['lastName']
        self.username = kwargs['username']
        self.email = kwargs['email']
        self.password = kwargs['password']


    def __repr__(self):
        return "<User: {}>".format(self.__tablename__)