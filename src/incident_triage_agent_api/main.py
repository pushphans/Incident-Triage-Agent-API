from incident_triage_agent_api.utils.rate_limiter import limiter
from incident_triage_agent_api.routers.ai_router import ai_router
from fastapi import FastAPI
from incident_triage_agent_api.routers.auth_router import auth_router

from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler




app = FastAPI()

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)


app.include_router(auth_router)
app.include_router(ai_router)

@app.get("/")
def root():
    return {
        "status" : "ok"
    }