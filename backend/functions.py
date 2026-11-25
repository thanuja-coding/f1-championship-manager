<<<<<<< HEAD
import jwt
import os

from datetime import datetime, timedelta, timezone


SECRET_KEY = os.getenv("SECRET_KEY", "f1_championship_secret_key")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRY = 30


def refresh_access_token(refresh_token):

    try:

        data = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if data.get("type") != "refresh":
            return None

        username = data.get("username")
        role = data.get("role")

        if not username or not role:
            return None

        expiry = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRY
        )

        access_token = jwt.encode(
            {
                "username": username,
                "role": role,
                "type": "access",
                "exp": expiry
            },
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return access_token

    except jwt.InvalidTokenError:

        return None
=======
from sqlalchemy import Integer, String, Column, create_engine, ForeignKey , Boolean
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
    
class Championships(Base):
    __tablename__ = "championships"

    championship_id = Column(Integer, primary_key=True)
    championship_name = Column(String)
    organizer_id = Column(Integer, ForeignKey("users.user_id"))

class ChampionshipTeams(Base):
    __tablename__ = "championship_teams"

    id = Column(Integer, primary_key=True)
    championship_id = Column(Integer, ForeignKey("championships.championship_id"))
    team_id = Column(Integer, ForeignKey("teams.team_id"))

class Races(Base):
    __tablename__ = "races"

    race_id = Column(Integer, primary_key=True)
    championship_id = Column(Integer, ForeignKey("championships.championship_id"))
    race_name = Column(String)
    race_date = Column(String)

class RaceResults(Base):
    __tablename__ = "race_results"

    result_id = Column(Integer, primary_key=True)
    race_id = Column(Integer, ForeignKey("races.race_id"))
    driver_id = Column(Integer, ForeignKey("drivers.driver_id"))
    team_id = Column(Integer, ForeignKey("teams.team_id"))
    position = Column(Integer)
    points = Column(Integer)
    fastest_lap = Column(Boolean, default=False)


Base.metadata.create_all(engine)


>>>>>>> d8d53a40bcfe5c1d1b067a492fc5049ef369c0a5
