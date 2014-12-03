from datetime import datetime

from sqlalchemy import Boolean, Column, Float
from sqlalchemy import Table, ForeignKey, UniqueConstraint
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import relationship, backref

import os

Session = None
ENGINE = None



engine = create_engine("mysql://root:db@dmin626@localhost/showhound", echo=False, convert_unicode=True)
session = scoped_session(sessionmaker(bind=engine,
                                      autocommit = False,
                                      autoflush = False))


Base = declarative_base()
Base.query = session.query_property()

class Shows(Base):
	__tablename__ = "shows"
	id = Column(Integer, primary_key=True)
	title = Column(String, nullable=True)
	summary = Column(Text, nullable=True )
	imdb_id = Column(String, nullable=True)
	network = Column(String, nullable=True)
 	airdate_start = Column(String, nullable=True)
	airdate_end = Column(String, nullable=True)
	genre = Column(String, nullable=True)
	imdb_id = Column(String, nullable=True)


class Series(Base):
	__tablename__ = "series"

	id = Column(Integer, primary_key=True)
	seriesid = Column(Integer, ForeignKey('shows.id'))
	title = Column(String, nullable=True)
	plot = Column(Text, nullable=True)
	origdate = Column(Text, nullable=True)
	season = Column(String, nullable=True)
	episode = Column(String, nullable=True)
	series = Column(String, nullable=True)
	nextairdate = Column(String, nullable=True)
	network = Column(String, nullable=True)
	poster = Column(String, nullable=True)
	posterid = Column(String, nullable=True)
	imdb_rating = Column(String, nullable=True)

	show = relationship("Shows", backref=backref("series", order_by=id))


class Users(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True)
	username = Column(String(100), nullable=False)
	email = Column(String(100), nullable=False)
	password = Column(String(100), nullable=False)
	first_name = Column(String(100), nullable=True)
	last_name = Column(String(100), nullable=True)
	cellphone = Column(String(20), nullable=True)
	zipcode = Column(String(15), nullable=True)
	# user = relationship("User", backref=backref("users_info", order_by=id))


class Config(object):
	DEBUG = False
	TESTING = False
	CSRF_ENABLED = True
	SECRET_KEY = 'this-really-needs-to-be-changed'



class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True



def connect():
    global ENGINE
    global Session
    ENGINE = create_engine("mysql://root:db@dmin626@localhost/showhound", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return session() 

# Creating tables in the engine
Base.metadata.create_all(engine)
