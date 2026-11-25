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


#A1 
def register_user(username: str, password: str, role: str):
    session = Session(engine)
    user_exists = session.query(User).filter_by(username = username).first()
    if user_exists is not None:
        session.close()
        return False

    try:
        hashed_password = ph.hash(password)
    except Exception:
        session.close()
        return False

    session.add(User(username=username, password=hashed_password, role=role))
    session.commit()
    session.close()
    return True


#admin
def create_admin():
    session = Session(engine)
    admin = session.query(User).filter_by(role="admin").first()
    if admin is None:
        session.add(User(username="admin", password=ph.hash("admin123"), role="admin"))
        session.commit()
    session.close()


#E2
def create_team(team_name, country, manager_id, driver_limit):
    session = Session(engine)
    manager = session.get(User, manager_id)
    team_exists = session.query(Teams).filter_by(team_name=team_name).first()
    if manager is None or team_exists is not None:
        session.close()
        return False

    new_team = Teams(team_name=team_name, country=country, manager_id=manager_id, driver_limit=driver_limit)
    session.add(new_team)
    session.commit()
    response = {
        "team_id": new_team.team_id,
        "team_name": new_team.team_name,
        "country": new_team.country,
        "manager_id": new_team.manager_id,
        "driver_limit": new_team.driver_limit
    }
    session.close()
    return response

#E3
def get_all_teams():
    session = Session(engine)
    response = []
    for team in session.query(Teams).all():
        response.append(team)
    session.close()
    return response

#E4
def get_team(team_id):
    session = Session(engine)
    team = session.get(Teams, team_id)
    if team is None:
        session.close()
        return None

    drivers = session.query(Drivers).filter_by(team_id=team_id).all()
    response = {
        "team_id": team.team_id,
        "team_name": team.team_name,
        "country": team.country,
        "manager_id": team.manager_id,
        "driver_limit": team.driver_limit,
        "drivers": drivers
    }
    session.close()
    return response

#E10
def register_team_for_championship(championship_id, team_id):
    session = Session(engine)
    already = session.query(ChampionshipTeams).filter_by(championship_id=championship_id, team_id=team_id).first()
    if already is not None:
        session.close()
        return False

    session.add(ChampionshipTeams(championship_id=championship_id, team_id=team_id))
    session.commit()
    session.close()
    return {"message": "Team registered for championship successfully"}

def get_championship(championship_id):
    session = Session(engine)
    championship = session.get(Championships, championship_id)
    session.close()
    return championship



