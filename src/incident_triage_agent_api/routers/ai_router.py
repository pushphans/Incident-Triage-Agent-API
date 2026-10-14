from fastapi import status
from fastapi import HTTPException
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from incident_triage_agent_api.utils.rate_limiter import limiter
from incident_triage_agent_api.schemas.ai_schemas import AiResponseSchema
from incident_triage_agent_api.ai.workflows.incident_triage_workflow import incident_workflow
from langchain.messages import HumanMessage
from incident_triage_agent_api.ai.state.incident_agent_state import IncidentAgentState
from incident_triage_agent_api.schemas.ai_schemas import AiRequestSchema
from incident_triage_agent_api.utils.dependency import get_current_user
from fastapi import Depends
from incident_triage_agent_api.models.auth_models import UserModel
from fastapi import APIRouter 


ai_router = APIRouter(tags=["AI"])

@ai_router.post("/chat")
@limiter.limit("10/minute")
async def chat(
    request : Request,
    data : AiRequestSchema,
    user : UserModel = Depends(get_current_user),
):  
    try:
        initial_state : IncidentAgentState = {
        "messages" : [HumanMessage(content=data.logs)],
        "parsed_logs" : None
    }

        final_state : IncidentAgentState = await incident_workflow.ainvoke(initial_state)

        return AiResponseSchema(
            solution=final_state['messages'][-1].content
        )

    except RateLimitExceeded:
        raise HTTPException(
            status_code = status.HTTP_429_TOO_MANY_REQUESTS,
            detail = "Too many requests"
        )

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = str(e)
        )

