from sqlalchemy import Column, String, Integer, create_engine, DateTime
from flask_sqlalchemy import SQLAlchemy
import os
import sys
import json

if os.environ['ENV'] == 'test':
    database_path = os.environ['TEST_DATABASE_URL']
else:
    database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
studio
Have bizname and release date
'''


class studio(db.Model):
    __tablename__ = 'studios'

    id = Column(Integer, primary_key=True)
    bizname = Column(String, nullable=False)
    opening_date = Column(DateTime(), nullable=False)

    def __init__(self, bizname, opening_date):
        self.bizname = bizname
        self.opening_date = opening_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'bizname': self.bizname,
            'opening_date': self.opening_date}


'''
instructor
Have name, age, and gender
'''


class instructor(db.Model):
    __tablename__ = 'instructors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender}
