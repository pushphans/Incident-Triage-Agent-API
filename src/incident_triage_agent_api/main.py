from fastapi import FastAPI
from incident_triage_agent_api.routers.auth_router import auth_router


app = FastAPI()


app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "status" : "ok"
    }