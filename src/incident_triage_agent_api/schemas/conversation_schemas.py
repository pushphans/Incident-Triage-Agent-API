from datetime import datetime
from uuid import UUID
import uuid
from pydantic import Field
from pydantic import BaseModel



class SaveConversationRequestSchema(BaseModel):
    title : str = Field(...)


class SaveConversationResponseModel(BaseModel):
    id : UUID
    title : str
    created_at : datetime
    updated_at : datetime



class UpdateConversationRequestSchema(BaseModel):
    title : str



class UpdateConversationResponseSchema(BaseModel):
    id : UUID
    title : str
    created_at : datetime
    updated_at : datetime