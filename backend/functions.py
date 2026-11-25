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

def create_token(username, token_type, role):
    time = ACCESS_TOKEN_EXPIRY

    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY

    payload = {
        "role": role,
        "username": username,
        "token_type": token_type,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=time)
    }

    token = jwt.encode(
        payload=payload,
        key=SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_token(token, token_type):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return False

    if payload["token_type"] == token_type:
        return payload

    return False

# A2 - Login
def verify_login(username, password):
    session = Session(engine)

    user = session.query(User).filter_by(username=username).first()

    if user is None:
        session.close()
        return False

    try:
        ph.verify(user.password, password)
    except VerifyMismatchError:
        session.close()
        return False

    access_token = create_token(username=username, token_type="access", role=user.role)
    refresh_token = create_token(username=username, token_type="refresh", role=user.role)

    session.close()

    return {"access_token": access_token, "refresh_token": refresh_token}

# E5 - Create Championship
def add_championship(championship_name, organizer_id):
    session = Session(engine)

    new_championship = Championships(championship_name=championship_name,organizer_id=organizer_id)

    session.add(new_championship)
    session.commit()

    response = {
        "championship_id": new_championship.championship_id,
        "championship_name": new_championship.championship_name,
        "organizer_id": new_championship.organizer_id
    }

    session.close()
    return response

# E6 - Get All Championships
def get_all_championships():
    session = Session(engine)

    response = []

    for championship in session.query(Championships).all():
        response.append({
            "championship_id": championship.championship_id,
            "championship_name": championship.championship_name,
            "organizer_id": championship.organizer_id
        })

    session.close()
    return response

# E7 - Register Driver Profile
def register_driver(user_id, full_name, nationality, racing_number):
    session = Session(engine)

    user = session.query(User).filter_by(user_id=user_id).first()

    if user is None:
        session.close()
        return False

    driver_exists = session.query(Drivers).filter_by(user_id=user_id).first()

    if driver_exists is not None:
        session.close()
        return False

    number_exists = session.query(Drivers).filter_by(racing_number=racing_number).first()

    if number_exists is not None:
        session.close()
        return False

    new_driver = Drivers(
        user_id=user_id,
        full_name=full_name,
        nationality=nationality,
        racing_number=racing_number
    )

    session.add(new_driver)
    session.commit()

    response = {
        "driver_id": new_driver.driver_id,
        "user_id": new_driver.user_id,
        "full_name": new_driver.full_name,
        "nationality": new_driver.nationality,
        "racing_number": new_driver.racing_number
    }

    session.close()
    return response

# E11 - Schedule Race in Championship
def add_race(championship_id, race_name, race_date):
    session = Session(engine)

    championship = session.query(Championships).filter_by(championship_id=championship_id).first()

    if championship is None:
        session.close()
        return False

    new_race = Races(
        championship_id=championship_id,
        race_name=race_name,
        race_date=race_date
    )

    session.add(new_race)
    session.commit()

    response = {
        "race_id": new_race.race_id,
        "championship_id": new_race.championship_id,
        "race_name": new_race.race_name,
        "race_date": new_race.race_date
    }

    session.close()
    return response

# E12 - Get Races for Championship
def get_races(championship_id):
    session = Session(engine)

    races = session.query(Races).filter_by(championship_id=championship_id).all()

    response = []

    for race in races:
        response.append({
            "race_id": race.race_id,
            "championship_id": race.championship_id,
            "race_name": race.race_name,
            "race_date": race.race_date
        })

    session.close()
    return response


