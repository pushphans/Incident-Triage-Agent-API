from datetime import datetime
from sqlalchemy import ForeignKey
import uuid
from sqlalchemy import Text, DateTime, UUID, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from incident_triage_agent_api.core.db import Base



class ConversationModel(Base):
    __tablename__ = "conversations"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key = True, nullable = False, default = uuid.uuid4)
    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable = False)
    title : Mapped[str] = mapped_column(Text, nullable = False) 
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), nullable = False)
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default = func.now(), onupdate = func.now(), nullable = False)


# class MessagesModel(Base):
#     id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
#     conversation_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable = False)
