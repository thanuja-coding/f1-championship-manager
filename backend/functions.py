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
    team_id = Column(Integer, ForeignKey("teams.team_id")) 
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

    drivers = []
    for application in session.query(Applications).filter_by(team_id=team_id, status="accepted").all():
        drivers.append(session.get(Drivers, application.driver_id))
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

def get_user(username):
    session = Session(engine)
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user

def get_championship(championship_id):
    session = Session(engine)
    championship = session.get(Championships, championship_id)
    session.close()
    return championship


# A3 - Refresh Access Token

def refresh_access_token(refresh_token):

    payload = verify_token(refresh_token, "refresh")

    if not payload:
        return False

    username = payload["username"]
    role = payload["role"]

    access_token = create_token(
        username=username,
        token_type="access",
        role=role
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# E8 - Apply to Join Team

def apply_to_team(driver_id, team_id):

    session = Session(engine)

    driver = session.query(Drivers).filter_by(
        driver_id=driver_id
    ).first()

    team = session.query(Teams).filter_by(
        team_id=team_id
    ).first()

    if driver is None or team is None:
        session.close()
        return False

    if driver.team_id is not None:
        session.close()
        return False

    current_drivers = session.query(Drivers).filter_by(
        team_id=team_id
    ).count()

    if current_drivers >= team.driver_limit:
        session.close()
        return False

    existing_application = session.query(Applications).filter_by(
        driver_id=driver_id,
        team_id=team_id,
        status="pending"
    ).first()

    if existing_application is not None:
        session.close()
        return False

    new_application = Applications(
        driver_id=driver_id,
        team_id=team_id,
        status="pending",
        applied_on=str(datetime.now(timezone.utc))
    )

    session.add(new_application)
    session.commit()

    response = {
        "application_id": new_application.application_id,
        "driver_id": new_application.driver_id,
        "team_id": new_application.team_id,
        "status": new_application.status,
        "applied_on": new_application.applied_on
    }

    session.close()

    return response


# E9 - Accept or Reject Application

def update_application(application_id, manager_id, decision):

    session = Session(engine)

    application = session.query(Applications).filter_by(
        application_id=application_id
    ).first()

    if application is None:
        session.close()
        return False

    team = session.query(Teams).filter_by(
        team_id=application.team_id
    ).first()

    if team is None or team.manager_id != manager_id:
        session.close()
        return False

    if application.status != "pending":
        session.close()
        return False

    if decision not in ["accepted", "rejected"]:
        session.close()
        return False

    if decision == "accepted":

        driver = session.query(Drivers).filter_by(
            driver_id=application.driver_id
        ).first()

        if driver is None or driver.team_id is not None:
            session.close()
            return False

        current_drivers = session.query(Drivers).filter_by(
            team_id=team.team_id
        ).count()

        if current_drivers >= team.driver_limit:
            session.close()
            return False

        driver.team_id = team.team_id

    application.status = decision

    session.commit()

    response = {
        "application_id": application.application_id,
        "driver_id": application.driver_id,
        "team_id": application.team_id,
        "status": application.status
    }

    session.close()

    return response


# E13 - Submit Race Results

def submit_race_result(race_id, driver_id, team_id, position, fastest_lap):

    session = Session(engine)

    race = session.query(Races).filter_by(
        race_id=race_id
    ).first()

    driver = session.query(Drivers).filter_by(
        driver_id=driver_id
    ).first()

    team = session.query(Teams).filter_by(
        team_id=team_id
    ).first()

    if race is None or driver is None or team is None:
        session.close()
        return False

    if driver.team_id != team_id:
        session.close()
        return False

    registered_team = session.query(ChampionshipTeams).filter_by(
        championship_id=race.championship_id,
        team_id=team_id
    ).first()

    if registered_team is None:
        session.close()
        return False

    existing_result = session.query(RaceResults).filter_by(
        race_id=race_id,
        driver_id=driver_id
    ).first()

    if existing_result is not None:
        session.close()
        return False

    if position < 1:
        session.close()
        return False

    points_table = {
        1: 25,
        2: 18,
        3: 15,
        4: 12,
        5: 10,
        6: 8,
        7: 6,
        8: 4,
        9: 2,
        10: 1
    }

    points = points_table.get(position, 0)


    new_result = RaceResults(
        race_id=race_id,
        driver_id=driver_id,
        team_id=team_id,
        position=position,
        points=points,
        fastest_lap=fastest_lap
    )

    session.add(new_result)
    session.commit()

    response = {
        "result_id": new_result.result_id,
        "race_id": new_result.race_id,
        "driver_id": new_result.driver_id,
        "team_id": new_result.team_id,
        "position": new_result.position,
        "points": new_result.points,
        "fastest_lap": new_result.fastest_lap
    }

    session.close()

    return response


# E14 - Get Championship Standings

def get_standings(championship_id):

    session = Session(engine)

    championship = session.query(Championships).filter_by(
        championship_id=championship_id
    ).first()

    if championship is None:
        session.close()
        return False

    results = session.query(RaceResults, Drivers).join(
        Drivers,
        RaceResults.driver_id == Drivers.driver_id
    ).join(
        Races,
        RaceResults.race_id == Races.race_id
    ).filter(
        Races.championship_id == championship_id
    ).all()

    standings = {}

    for result, driver in results:

        driver_id = driver.driver_id

        if driver_id not in standings:

            standings[driver_id] = {
                "driver_id": driver.driver_id,
                "full_name": driver.full_name,
                "racing_number": driver.racing_number,
                "total_points": 0,
                "wins": 0,
                "podiums": 0,
                "races_completed": 0
            }

        standings[driver_id]["total_points"] += result.points
        standings[driver_id]["races_completed"] += 1

        if result.position == 1:
            standings[driver_id]["wins"] += 1

        if result.position <= 3:
            standings[driver_id]["podiums"] += 1

    response = list(standings.values())

    response.sort(
        key=lambda x: x["total_points"],
        reverse=True
    )

    session.close()

    return response


# E15 - Get Driver Performance History

def get_driver_performance(username):

    session = Session(engine)

    user = session.query(User).filter_by(
        username=username
    ).first()

    if user is None:
        session.close()
        return False

    driver = session.query(Drivers).filter_by(
        user_id=user.user_id
    ).first()

    if driver is None:
        session.close()
        return False

    results = session.query(RaceResults, Races).join(
        Races,
        RaceResults.race_id == Races.race_id
    ).filter(
        RaceResults.driver_id == driver.driver_id
    ).all()

    response = []

    for result, race in results:

        response.append({
            "race_id": race.race_id,
            "race_name": race.race_name,
            "championship_id": race.championship_id,
            "position": result.position,
            "points": result.points,
            "fastest_lap": result.fastest_lap
        })

    session.close()

    return {
        "driver_id": driver.driver_id,
        "full_name": driver.full_name,
        "racing_number": driver.racing_number,
        "performance": response
    }


