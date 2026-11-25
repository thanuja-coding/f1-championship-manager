from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

import functions

class TeamApplication(BaseModel):

    team_id: int


app = FastAPI()


class RefreshRequest(BaseModel):

    refresh_token: str


@app.get("/")
def home():

    return {"message": "F1 Championship Manager API"}


@app.post("/auth/refresh")
def refresh_token(data: RefreshRequest):

    access_token = functions.refresh_access_token(
        data.refresh_token
    )

    if not access_token:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired refresh token"
        )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }