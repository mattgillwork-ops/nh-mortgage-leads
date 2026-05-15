from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import lead_manager
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Lead(BaseModel):
    loan_purpose: str
    property_type: str
    location_nh: str
    est_value: float
    down_payment: float
    credit_score: str
    first_name: str
    last_name: str
    email: str
    phone: str

@app.post("/submit_lead")
async def submit_lead(lead: Lead):
    try:
        lead_manager.save_lead(lead.model_dump())
        return {"status": "success", "message": "Lead captured successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export")
async def export_leads():
    try:
        path = lead_manager.export_to_csv()
        return {"status": "success", "file": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    lead_manager.init_db()
    uvicorn.run(app, host="0.0.0.0", port=8001)
