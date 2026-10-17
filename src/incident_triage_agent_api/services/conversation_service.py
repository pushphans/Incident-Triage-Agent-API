from fastapi import Query
from uuid import UUID
from incident_triage_agent_api.schemas.conversation_schemas import UpdateConversationResponseSchema
from sqlalchemy import select
from incident_triage_agent_api.schemas.conversation_schemas import UpdateConversationRequestSchema
from incident_triage_agent_api.schemas.conversation_schemas import SaveConversationResponseModel
from incident_triage_agent_api.models.ai_models import ConversationModel
from incident_triage_agent_api.schemas.conversation_schemas import SaveConversationRequestSchema
import uuid
from sqlalchemy.ext.asyncio import AsyncSession



class ConversationNotFound(Exception):
    pass



async def save_conversation(
    db : AsyncSession,
    user_id : uuid.UUID,
    data : SaveConversationRequestSchema
):
   try:
        conversation = ConversationModel(
            user_id = user_id,
            title = data.title
        )


        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)

        return SaveConversationResponseModel(
            id=conversation.id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )

   except Exception as e:
    await db.rollback()
    raise





async def update_conversation(
    db : AsyncSession,
    con_id : uuid.UUID,
    user_id : uuid.UUID,
    data : UpdateConversationRequestSchema
):
    try:
        query = (
            select(ConversationModel)
            .where(ConversationModel.id == con_id, ConversationModel.user_id == user_id)
        )

        result = await db.execute(query)

        conversation_exists = result.scalar_one_or_none()

        if conversation_exists is None:
            raise ConversationNotFound()

        
        conversation_exists.title = data.title

        await db.commit()

        await db.flush()

        return UpdateConversationResponseSchema(
            id=conversation_exists.id,
            title=conversation_exists.title,
            created_at=conversation_exists.created_at,
            updated_at=conversation_exists.created_at
        )


    except Exception:
        await db.rollback()
        raise 




async def delete_conversation(
    db : AsyncSession,
    user_id : UUID,
    con_id : UUID
):
    query = (
        select(ConversationModel)
        .where(ConversationModel.user_id == user_id, ConversationModel.id == con_id)
    )

    result = await db.execute(query)

    conversation = result.scalar_one_or_none()

    if conversation is None:
        raise ConversationNotFound()

    await db.delete(conversation)
    await db.commit()

    return True



async def list_conversations(
    db : AsyncSession,
    user_id : UUID, 
    search_term : str | None, 
    page_size : int = Query(default=10, ge=1, le=100),
    page_number : int = Query(default=1, ge=1),

):

    try:
        query = (
            select(ConversationModel)
            .where(ConversationModel.user_id == user_id)
        )

        if search_term is not None:
            query = (
                query.where(ConversationModel.title.ilike(f"%{search_term}%"))
            )

        
        offset = (page_number-1) * page_size

        query = query.offset(offset).limit(page_size)

        result = await db.execute(query)

        conversatons = result.scalars().all()

        return conversatons
    
    except Exception:
        await db.rollback()
        raise




async def get_conversation(
    db : AsyncSession,
    user_id : UUID,
    id : UUID
):
    try:
        query = (
        select(ConversationModel)
        .where(ConversationModel.id == id, ConversationModel.user_id == user_id)
    )

        result = await db.execute(query)

        conversation = result.scalar_one_or_none()

        if conversation is None:
            raise LookupError()

        return conversation

    except Exception:
        await db.rollback()
        raise