# coding=utf-8
from app import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from app.utils.generate_uuid import generate_uuid



class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.String, primary_key=True, default=generate_uuid, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                          default=datetime.utcnow, onupdate=datetime.utcnow)


    def save(self):
        """Save an instance of the model to the database."""
        try:
            db.session.add(self)
            return db.session.commit()
        except SQLAlchemyError:
            return db.session.rollback()

        
    def delete(self):
        """Delete an instance of the model from the database."""
        try:
            db.session.delete(self)
            return db.session.commit()
        except SQLAlchemyError:
            return db.session.rollback()

    
    @classmethod
    def get_all(cls):
        """Return all the data in the model."""
        return cls.query.all()

    @classmethod
    def get_one(cls, data):
        """Return all the data in the model."""
        return cls.query.get(data)

    
    @classmethod
    def filter_by_any(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()
