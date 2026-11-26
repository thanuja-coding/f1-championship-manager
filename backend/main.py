from fastapi import FastAPI , HTTPException , Header , Body
from pydantic import BaseModel , Field
from datetime import date
import functions


app = FastAPI(
    title = "F1 Championship Manager API",
    description="Manage racing teams, drivers, championships, races, results and standings",
)
ROLES = ["admin", "driver"]




def authorize(token, allowed_roles):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired token")
    if payload["role"] not in allowed_roles:
        raise HTTPException(status_code=403, detail="You do not have permission to do this")
    return payload

class RefreshRequest(BaseModel):
    refresh_token: str


class ApplicationDecision(BaseModel):
    decision: str


class RaceResultRequest(BaseModel):
    driver_id: int = Field(gt=0)
    team_id: int = Field(gt=0)
    position: int = Field(gt=0)
    fastest_lap: bool = False

class UserCreate(BaseModel):
    username: str = Field(min_length=2)
    password: str = Field(min_length=6)
    role: str = "driver"


class OrganizerCreate(BaseModel):
    username: str = Field(min_length=2)
    password: str = Field(min_length=6)


class TeamCreate(BaseModel):
    team_name: str = Field(min_length=2)
    country: str = Field(min_length=2)
    manager_id: int = Field(gt=0)
    driver_limit: int = Field(gt=0)


class ChampionshipTeamCreate(BaseModel):
    team_id: int = Field(gt=0)


#A1
@app.post("/auth/register")
def register_user(user: UserCreate):
    if user.role not in ROLES:
        raise HTTPException(status_code=400,detail="Role must be admin or driver")
    if functions.register_user(username=user.username,password=user.password,role=user.role):
        return {"message":"user registered successfully"}
    raise HTTPException(status_code=409,detail="User already exists")

#E1
@app.post("/admin/organizers")
def create_organizer(organizer: OrganizerCreate , token = Header(None)):
    authorize(token, ["admin"])
    if functions.register_user(username=organizer.username,password=organizer.password,role="organizer"):
        return {"message":"organizer created successfully"}
    raise HTTPException(status_code=409,detail="User already exists")

#E2
@app.post("/teams")
def create_team(team: TeamCreate , token = Header(None)):
    authorize(token, ["admin"])
    response = functions.create_team(team_name=team.team_name , country=team.country , manager_id=team.manager_id , driver_limit=team.driver_limit)
    if not response:
        raise HTTPException(status_code=400,detail="Team already exists or manager not found")
    return response

#E3
@app.get("/teams")
def teams():
    return functions.get_all_teams()

#E4
@app.get("/teams/{team_id}")
def team(team_id:int):
    if functions.get_team(team_id=team_id) is None:
        raise HTTPException(status_code=404,detail="Team not found")
    return functions.get_team(team_id=team_id)

#E10
@app.post("/championships/{championship_id}/teams")
def register_team(championship_id:int , data: ChampionshipTeamCreate , token = Header(None)):
    payload = authorize(token, ["driver"])
    if functions.get_championship(championship_id=championship_id) is None:
        raise HTTPException(status_code=404,detail="Championship not found")
    if functions.get_team(team_id=data.team_id) is None:
        raise HTTPException(status_code=404,detail="Team not found")
    if functions.get_team(team_id=data.team_id)["manager_id"] != functions.get_user(username=payload["username"]).user_id:
        raise HTTPException(status_code=403,detail="Only the team manager can register the team")
    response = functions.register_team_for_championship(championship_id=championship_id , team_id=data.team_id)
    if not response:
        raise HTTPException(status_code=409,detail="Team already registered for this championship")
    return response

    # A3 - Refresh Access Token
@app.post("/auth/refresh")
def refresh_token(data: RefreshRequest):
    response = functions.refresh_access_token(
        refresh_token=data.refresh_token
    )

    if not response:
        raise HTTPException(status_code=401, detail="Invalid or Expired refresh token")

    return response

# E8 - Apply to Join Team
@app.post("/teams/{team_id}/apply")
def apply_team(team_id: int, token=Header(None)):
    payload = authorize(token, ["driver"])

    user = functions.get_user(username=payload["username"])

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    driver = functions.get_driver_by_user_id(user_id=user.user_id)

    if driver is None:
        raise HTTPException(status_code=404, detail="Driver profile not found")

    response = functions.apply_to_team(
        driver_id=driver.driver_id,
        team_id=team_id
    )

    if not response:
        raise HTTPException(status_code=400, detail="Unable to apply for team")

    return response

    # E9 - Accept or Reject Application
@app.put("/applications/{application_id}")
def manage_application(
    application_id: int,
    data: ApplicationDecision,
    token=Header(None)
):
    payload = authorize(token, ["driver", "admin"])

    user = functions.get_user(username=payload["username"])

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    response = functions.update_application(
        application_id=application_id,
        manager_id=user.user_id,
        decision=data.decision
    )

    if not response:
        raise HTTPException(status_code=400, detail="Unable to update application")

    return response


# E13 - Submit Race Results
@app.post("/races/{race_id}/results")
def add_race_result(
    race_id: int,
    data: RaceResultRequest,
    token=Header(None)
):
    authorize(token, ["organizer"])

    response = functions.submit_race_result(
        race_id=race_id,
        driver_id=data.driver_id,
        team_id=data.team_id,
        position=data.position,
        fastest_lap=data.fastest_lap
    )

    if not response:
        raise HTTPException(status_code=400, detail="Unable to submit race result")

    return response

# E14 - Get Championship Standings
@app.get("/championships/{championship_id}/standings")
def championship_standings(championship_id: int):
    response = functions.get_standings(
        championship_id=championship_id
    )

    if response is False:
        raise HTTPException(status_code=404, detail="Championship not found")

    return response

# E14 - Get Championship Standings
@app.get("/championships/{championship_id}/standings")
def championship_standings(championship_id: int):
    response = functions.get_standings(
        championship_id=championship_id
    )

    if response is False:
        raise HTTPException(status_code=404, detail="Championship not found")

    return response
    
# E15 - Get Driver Performance
@app.get("/drivers/{username}/performance")
def driver_performance(username: str):
    response = functions.get_driver_performance(
        username=username
    )

    if response is False:
        raise HTTPException(status_code=404, detail="Driver not found")

    return response



