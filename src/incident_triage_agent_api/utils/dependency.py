from incident_triage_agent_api.models.auth_models import UserModel
from sqlalchemy import select
from fastapi import status
from fastapi.responses import JSONResponse
from incident_triage_agent_api.utils.tokens_security import decode_jwt
from incident_triage_agent_api.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials



security = HTTPBearer()



async def get_current_user(
    credentials : HTTPAuthorizationCredentials = Depends(security),
    db : AsyncSession = Depends(get_db)
):

    token = credentials.credentials

    payload = await decode_jwt(token=token)

    user_id = payload.get("sub")

    if user_id is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail" : "Invalid token"}
        )

    query = (
        select(UserModel)
        .where(UserModel.id == user_id)
    )

    result = await db.execute(query)

    user = result.scalar_one_or_none()

    if user is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail" : "User not found"}
        )

    return user


