from datetime import datetime
from uuid import UUID
import uuid
from pydantic import Field
from pydantic import BaseModel



class AiRequestSchema(BaseModel):
    logs : str = Field(...)



class AiResponseSchema(BaseModel):
    solution : str




    