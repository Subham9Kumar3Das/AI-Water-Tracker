from fastapi import FastAPI
from src.agent import WaterIntakeAgent
from pydantic import BaseModel
from src.database import log_intake, get_intake
from src.logger import log_message, log_error

app = FastAPI()
agent = WaterIntakeAgent()

class WaterIntakeRequest(BaseModel):
    user_id: str
    intake_ml: int


@app.post("/log_intake")
async def log_water_intake(request: WaterIntakeRequest):
    log_intake(request.user_id, request.intake_ml)
    analysis = agent.analyze_intake(request.intake_ml)
    log_message(f"User {request.user_id} logged {request.intake_ml}ml")
    return {"message": "water intake logged successfully", "analysis": analysis}


@app.get("/history/{user_id}")
async def get_water_intake_history(user_id: str):
    history = get_intake_history(user_id)
    return {"user_id": user_id, "history": history}