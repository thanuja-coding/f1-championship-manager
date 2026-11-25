import jwt
import os

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, Session
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