from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker, scoped_session

from werkzeug import generate_password_hash, check_password_hash

ENGINE = create_engine("postgresql://rxdt@localhost/gitviz_db", echo=True)
session = scoped_session(sessionmaker(bind=ENGINE, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()




class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key = True) # make this a UUID
  username = Column(String(64), nullable=False) # make this false
  password = Column(String(64), nullable=False) # make this false

  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)

  def set_password(self, password):
    self.password = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.password, password)





def main():
  """In case we need this for something"""
  pass


if __name__ == "__main__":
  main()