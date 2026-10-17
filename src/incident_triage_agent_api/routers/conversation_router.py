from pydantic import Field
from fastapi.responses import JSONResponse
from incident_triage_agent_api.schemas.conversation_schemas import UpdateConversationRequestSchema
from uuid import UUID
from fastapi import status
from fastapi import HTTPException
from incident_triage_agent_api.services import conversation_service
from incident_triage_agent_api.schemas.conversation_schemas import SaveConversationRequestSchema
from incident_triage_agent_api.utils.dependency import get_current_user
from incident_triage_agent_api.models.auth_models import UserModel
from incident_triage_agent_api.core.db import get_db
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter

con_router = APIRouter(tags=["CONVERSTIONS"])






@con_router.post("/conversation")
async def execute_add_conversation(
    data : SaveConversationRequestSchema,
    db : AsyncSession = Depends(get_db),
    user : UserModel = Depends(get_current_user)
):
    try:
        result = conversation_service.save_conversation(data=data, db=db, user_id=user.id)
        return result

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e)
        )


@con_router.put("/conversation")
async def execute_update_conversation(
    con_id : UUID,
    data : UpdateConversationRequestSchema,
    db : AsyncSession = Depends(get_db),
    user : UserModel = Depends(get_current_user),
):

    try:
        result = await conversation_service.update_conversation(con_id=con_id, db=db, data=data, user_id=user.id)
        return result

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e)
        )



@con_router.delete("/conversation/{id}")
async def execute_delete_conversation(
    con_id : UUID,
    db : AsyncSession = Depends(get_db),
    user : UserModel = Depends(get_current_user),
):
    result = await conversation_service.delete_conversation(user_id=user.id, con_id=con_id, db=db)

    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Conversation not found"
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail" : "Conversation deleted successfully"}
    )




@con_router.get("/conversations")
async def execute_list_conversation(
    search_term : str | None,
    db : AsyncSession = Depends(get_db),
    user : UserModel = Depends(get_current_user),
    page_number : int = Field(default=1, ge=1, le=100),
    page_size : int = Field(default = 10, ge=1), 
):
    try:
        result = await conversation_service.list_conversations(
            db=db, 
            user_id=user.id, 
            page_number=page_number, 
            page_size=page_size, 
            search_term=search_term
        )
        return result


    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e)
        )





@con_router.get("/conversation/{id}")
async def get_conversation(
    id : UUID,
    db : AsyncSession = Depends(get_db),
    user : UserModel = Depends(get_current_user)
):
    try:
        result = await conversation_service.get_conversation(user_id=user.id, db=db, id=id)
        return result


    except LookupError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Coversations not found"
        )

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e)
        )