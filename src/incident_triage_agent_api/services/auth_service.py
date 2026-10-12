from incident_triage_agent_api.schemas.auth_schemas import TokenRefreshResponseSchema
from incident_triage_agent_api.schemas.auth_schemas import TokenRefreshRequestSchema
from incident_triage_agent_api.schemas.auth_schemas import LoginResponseModel
from datetime import timedelta
from datetime import timezone
from datetime import datetime
from incident_triage_agent_api.utils.tokens_security import create_refresh_token
from incident_triage_agent_api.models.auth_models import RefreshTokenModel
from incident_triage_agent_api.core.config import settings
from incident_triage_agent_api.utils.tokens_security import create_access_token
from incident_triage_agent_api.utils.password_security import verify_password
from incident_triage_agent_api.schemas.auth_schemas import LoginRequestSchema
from sqlalchemy import select
from incident_triage_agent_api.schemas.auth_schemas import RegisterResponseSchema
from incident_triage_agent_api.models.auth_models import UserModel
from incident_triage_agent_api.schemas.auth_schemas import RegisterRequestModel
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from incident_triage_agent_api.utils.password_security import hash_password, verify_password 



class EmailAlreadyExistsError(Exception):
    pass

class InvalidCredentialError(Exception):
    pass


class RefreshTokenNotFoundError(Exception):
    pass



async def register(
    db : AsyncSession,
    data : RegisterRequestModel
):

    try:
        query = (
            select(UserModel)
            .where(UserModel.email == data.email)
        )

        result = await db.execute(query)

        user_exists = result.scalar_one_or_none()

        if user_exists:
            raise EmailAlreadyExistsError()

        hashed_password = await hash_password(password=data.password)


        user = UserModel(
        name = data.name,
        email = data.email,
        password_hash = hashed_password
    )

        db.add(user)
        await db.commit()
        await db.refresh(user)

        return RegisterResponseSchema(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    except Exception:
        await db.rollback()
        raise


async def login(
    db : AsyncSession,
    data : LoginRequestSchema
):
    try:
        email_exists_query = (
        select(UserModel)
        .where(UserModel.email == data.email)
        )


        email_exists_result = await db.execute(email_exists_query)

        email_exists = email_exists_result.scalar_one_or_none()

        if email_exists is None:
            raise InvalidCredentialError()

        password_verification = await verify_password(
            hashed_password=email_exists.password_hash, 
            password=data.password
        )

        if not password_verification:
            raise InvalidCredentialError()

        access_token = await create_access_token(user_id=email_exists.id)
        access_token_expiry = settings.ACCESS_TOKEN_EXPIRY_IN_MINUTES * 60

        new_refresh_token = await create_refresh_token()
        new_refresh_token_expiry = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRY_IN_DAYS)

        refresh_token_check_query = (
            select(RefreshTokenModel)
            .where(RefreshTokenModel.user_id == email_exists.id)
        )

        refresh_token_exists_result = await db.execute(refresh_token_check_query)

        refresh_token_exists = refresh_token_exists_result.scalar_one_or_none()

        if refresh_token_exists is None:

            refresh_token_exists = RefreshTokenModel(
            user_id = email_exists.id,
            refresh_token = new_refresh_token,
            expiry = new_refresh_token_expiry,
            )

            db.add(refresh_token_exists)

        refresh_token_exists.refresh_token = new_refresh_token
        refresh_token_exists.expiry = new_refresh_token_expiry

        await db.commit()
        await db.refresh(refresh_token_exists)

        return LoginResponseModel(
            user_id=refresh_token_exists.user_id,
            name=email_exists.name,
            email=email_exists.email,
            refresh_token=refresh_token_exists.refresh_token,
            access_token=access_token,
            access_token_expiry=access_token_expiry,
            created_at=email_exists.created_at,
            updated_at=email_exists.updated_at
        )

    except Exception:
        await db.rollback()
        raise





async def refresh_token(
    db : AsyncSession,
    data : TokenRefreshRequestSchema
):
    try:
        refresh_token_check_query = (
            select(RefreshTokenModel)
            .where(
                RefreshTokenModel.refresh_token == data.refresh_token
            )
        )

        refresh_token_exists_result = await db.execute(refresh_token_check_query)


        refresh_token_exists = refresh_token_exists_result.scalar_one_or_none()

        if refresh_token_exists is None:
            raise RefreshTokenNotFoundError()

        if refresh_token_exists.expiry <= datetime.now(timezone.utc):
            raise RefreshTokenNotFoundError()

        new_access_token = await create_access_token(user_id=refresh_token_exists.user_id)
        new_access_token_expiry = settings.ACCESS_TOKEN_EXPIRY_IN_MINUTES * 60

        return TokenRefreshResponseSchema(
            access_token=new_access_token,
            access_token_expiry=new_access_token_expiry,
            refresh_token=refresh_token_exists.refresh_token
        )

    except Exception:
        await db.rollback()
        raise

        
    
    





