from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from werkzeug import generate_password_hash, check_password_hash

ENGINE = create_engine("postgresql://rxdt@localhost/gitviz_db", echo=True)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

db = SQLAlchemy()

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key = True) # make this a UUID
  username = Column(String(64), nullable=False) # make this false
  password = Column(String(512), nullable=False) # make this false

  def __init__(self, username, password):
    self.username = username.lower()
    self.set_password(password)

  def set_password(self, password):
    self.password = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.password, password)

  def __repr__(self):
    return "<User %r>" % self.username




def main():
  """In case we need this for something"""
  pass


if __name__ == "__main__":
  main()