from sqlalchemy import Integer, String, Column, create_engine, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime, timedelta, timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


ph = PasswordHasher()

DB_PATH = "f1_championship.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


ACCESS_TOKEN_EXPIRY = 15
REFRESH_TOKEN_EXPIRY = 7*24*60
SECRET_KEY = "SECRETCODE"
ALGORITHM = "HS256"

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="driver")

class Teams(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True)
    team_name = Column(String, unique=True)
    country = Column(String)
    manager_id = Column(Integer, ForeignKey("users.user_id"))
    driver_limit = Column(Integer)

class Drivers(Base):
    __tablename__ = "drivers"

    driver_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    full_name = Column(String)
    nationality = Column(String)
    racing_number = Column(Integer, unique=True)

class Applications(Base):
    __tablename__ = "applications"

    application_id = Column(Integer, primary_key=True)
    driver_id = Column(Integer, ForeignKey("drivers.driver_id"))
    team_id = Column(Integer, ForeignKey("teams.team_id"))
    status = Column(String, default="pending")
    applied_on = Column(String)

Base.metadata.create_all(engine)