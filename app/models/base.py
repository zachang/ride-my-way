# coding=utf-8
from app import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError


class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.String, primary_key=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime,
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
    def filter_by_username(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def filter_by_email(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()