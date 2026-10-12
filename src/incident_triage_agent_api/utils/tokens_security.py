import secrets
from datetime import timedelta
from datetime import datetime, timezone
import jwt
from incident_triage_agent_api.core.config import settings
from uuid import UUID


async def create_access_token(user_id : UUID):
    payload = {
        "sub" : str(user_id),
        "exp" : datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_IN_MINUTES)
    }

    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


    return token



async def decode_jwt(token : str):
    return jwt.decode(
        token,
        algorithms=[settings.ALGORITHM],
        key=settings.JWT_SECRET_KEY,
    )



async def create_refresh_token():
    return secrets.token_urlsafe(64)