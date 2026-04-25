"""EVEZ Credit Scoring API — FastAPI Application"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import evez_credit_engine as engine

app = FastAPI(
    title="EVEZ Credit Scoring API",
    version="2.0.0",
    description="Production-ready FICO-equivalent credit scoring with ECOA/FCRA compliance"
)

class ApplicantInput(BaseModel):
    id: Optional[str] = None
    payment_history: float = 85.0
    credit_utilization: float = 30.0
    credit_age: float = 5.0
    credit_mix: int = 3
    new_inquiries: int = 1
    dti_ratio: float = 30.0
    derogatory_marks: int = 0
    total_accounts: int = 8
    annual_income: Optional[float] = None
    requested_amount: Optional[float] = None

class BatchRequest(BaseModel):
    applicants: Optional[List[ApplicantInput]] = None
    count: int = 10

@app.get("/health")
async def health():
    return {"status": "ok", "version": "2.0.0", "model": "EVEZ-CS-v2.0"}

@app.post("/score")
async def score_applicant(applicant: ApplicantInput):
    return engine.score_applicant(applicant.dict())

@app.post("/batch")
async def batch_score(request: BatchRequest):
    if request.applicants:
        results = [engine.score_applicant(a.dict()) for a in request.applicants]
        return {"results": results, "count": len(results)}
    return engine.batch_score(request.count)

@app.get("/model-info")
async def model_info():
    return {
        "version": "EVEZ-CS-v2.0",
        "factors": list(engine.RISK_FACTORS.keys()),
        "weights": {k: v["weight"] for k, v in engine.RISK_FACTORS.items()},
        "score_range": list(engine.SCORE_RANGE),
        "grade_thresholds": engine.GRADE_THRESHOLDS,
        "compliance": ["ECOA", "FCRA", "Reg B", "Fair Lending"]
    }