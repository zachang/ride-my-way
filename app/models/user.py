from passlib.hash import pbkdf2_sha256 as sha256
from app import db
from app.models.base import Base
from app.models.ride import Ride
from app.models.rate import Rate
from app.models.request import Request


class User(Base):
    """Define fields for User."""

    __tablename__ = "user"

    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    username = db.Column(db.String(250), unique=True, nullable=False)
    phone_no = db.Column(db.String(50), unique=True , nullable=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    user_image = db.Column(db.String(200), nullable=True)
    is_social = db.Column(db.Boolean, default=False, nullable=True)
    reg_type = db.Column(db.String(50), default='regular', nullable=True)
    rides = db.relationship('Ride', backref='user', lazy=True, cascade='all, delete-orphan')
    rates = db.relationship('Rate', backref='user', lazy=True)
    request = db.relationship('Request', backref='user', lazy=True)


    def __init__(self, **kwargs):
        """initialize class."""
        self.first_name = kwargs['first_name']
        self.last_name = kwargs['last_name']
        self.username = kwargs['username']
        self.email = kwargs['email']
        self.password = kwargs['password']


    def __repr__(self):
        return "<User: {}>".format(self.__tablename__)


    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

        
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)
