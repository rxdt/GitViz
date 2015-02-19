from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from werkzeug import generate_password_hash, check_password_hash

import base64


ENGINE = create_engine("postgresql://rxdt@localhost/gitviz_db", echo=True)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))
session._model_changes = {}

Base = declarative_base()
Base.query = session.query_property()

db = SQLAlchemy()

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key = True)
  username = Column(String(64), nullable=False)
  password = Column(String(512), nullable=False)
  authenticated = db.Column(db.Boolean, default=False)
  github_access_token = Column(String(200), default=None)

  def __init__(self, username, password):
    self.username = username.lower()
    self.set_password(password)
    self.authenticated = True

  def set_github_access_token(self, github_access_token):
    self.github_access_token = github_access_token

  def set_password(self, password):
    self.password = generate_password_hash(str(password))
   
  def check_password(self, password):
    return check_password_hash(self.password, password)

  def __repr__(self):
    return "<User %r>" % self.username

  def is_active(self):
    return True

  def get_id(self):
    return self.id

  def is_authenticated(self):
    return self.authenticated

  def is_anonymous(self): 
    return False


def main():
  """In case we need this for something"""
  pass


if __name__ == "__main__":
  main()