"""
https://pythonspot.com/login-authentication-with-flask/
"""
#from sqlalchemy import *
#from sqlalchemy import create_engine, ForeignKey
#from sqlalchemy import Column, Date, Integer, String
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import relationship, backref

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import SQLITE_FILE

engine = create_engine(f"sqlite:///{SQLITE_FILE}", echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Job(Base):
    __tablename__ = "job"

    id = Column(Integer, primary_key=True)
    driver = Column(String)   # driver
    sername = Column(String)  # series name
    simname = Column(String)  # simulation name
    configfile = Column(String)  # path to the config file on disc
                                 # will be renamed to simname.config
    submit_date = Column(Date)

    def __init__(self, driver, sername, simname, configfile, submit_date):
        self.driver = driver
        self.sername = sername
        self.simname = simname
        self.configfile = configfile
        self.submit_date = submit_date


# create tables
Base.metadata.create_all(engine)
