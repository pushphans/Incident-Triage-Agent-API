from sqlalchemy import ForeignKey
from pydantic import EmailStr
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, DateTime, Boolean, func, UUID
from incident_triage_agent_api.core.db import Base
import uuid
from datetime import datetime


class UserModel(Base):
    __tablename__ = "users"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key = True, default = uuid.uuid4, nullable = False)
    name : Mapped[str] = mapped_column(Text, nullable = False)
    email : Mapped[EmailStr] = mapped_column(Text, unique = True, index = True, nullable = False)
    password_hash : Mapped[str] = mapped_column(Text, nullable = False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), nullable = False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), onupdate = func.now(), nullable = False)




class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key = True, nullable = False, default = uuid.uuid4)
    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index = True, nullable = False)
    refresh_token : Mapped[str] = mapped_column(Text, unique = True, index = True, nullable = False)
    expiry : Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable = False)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), nullable = False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), onupdate = func.now(), nullable = False)

