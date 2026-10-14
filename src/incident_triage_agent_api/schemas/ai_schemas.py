from pydantic import Field
from pydantic import BaseModel



class AiRequestSchema(BaseModel):
    logs : str = Field(...)



class AiResponseSchema(BaseModel):
    solution : str