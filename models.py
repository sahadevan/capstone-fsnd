import os
from sqlalchemy import Column, String, Integer, Date
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

DB_PATH = os.getenv('DB_PATH', 'postgresql+psycopg2://postgres:admin@localhost:5432/casting')

database_path = DB_PATH
db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    migrate = Migrate(app, db)
    db.init_app(app)  
    return db

"""
Movies

"""
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    casts = db.relationship('Cast', backref='movie', lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return { 'id': self.id, 'title': self.title, 'release_date': self.release_date }

    def short(self):
        return { 'title': self.title, 'release_date': self.release_date }

    def __repr__(self):
         return f'<Movie {self.id} title: {self.title} release_date: {self.release_date}>'

"""
Actor

"""
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    casts = db.relationship('Cast', backref='actor', lazy=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return { 'id': self.id, 'name': self.name, 'age': self.age, 'gender': self.gender }
    
    def short(self):
        return { 'name': self.name, 'age': self.age, 'gender': self.gender }

    def __repr__(self):
         return f'<Actor {self.id} name: {self.name} age: {self.age} gender: {self.gender}>'
    
"""
Cast

"""
class Cast(db.Model):
  __tablename__ = 'casts'

  id = db.Column(db.Integer, primary_key=True)
  movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
  actor_id = db.Column(db.Integer, db.ForeignKey('actors.id'), nullable=False)

  def __repr__(self):
    return f'<Cast {self.id} movie_id: {self.movie_id} actor_id: {self.actor_id}>'