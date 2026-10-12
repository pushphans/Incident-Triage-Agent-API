from incident_triage_agent_api.services.auth_service import RefreshTokenNotFoundError
from incident_triage_agent_api.schemas.auth_schemas import TokenRefreshRequestSchema
from incident_triage_agent_api.services.auth_service import InvalidCredentialError
from incident_triage_agent_api.schemas.auth_schemas import LoginRequestSchema
from incident_triage_agent_api.services.auth_service import EmailAlreadyExistsError
from fastapi import status
from fastapi import HTTPException
from incident_triage_agent_api.services import auth_service
from incident_triage_agent_api.schemas.auth_schemas import RegisterRequestModel
from incident_triage_agent_api.core.db import get_db
from incident_triage_agent_api.models.auth_models import UserModel
from incident_triage_agent_api.utils.dependency import get_current_user
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter


auth_router = APIRouter(tags=["AUTH"])


@auth_router.post("/register")
async def register(
    data : RegisterRequestModel,
    db : AsyncSession = Depends(get_db),
):
    try:
        user = await auth_service.register(data=data, db=db)
        return user

    except EmailAlreadyExistsError:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Email already exists"
        ) 

    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )



@auth_router.post("/login")
async def login(
    data : LoginRequestSchema,
    db : AsyncSession = Depends(get_db),
):
    try:
        result = await auth_service.login(data=data, db=db)
        return result

    except InvalidCredentialError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials"
        )

    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )


@auth_router.post("/refresh-token")
async def refresh_token(
    data : TokenRefreshRequestSchema,
    db : AsyncSession = Depends(get_db)
):
    try:
        result = await auth_service.refresh_token(data=data, db=db)
        return result

    except RefreshTokenNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid credentials"
        )

    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )