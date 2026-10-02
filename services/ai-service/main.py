import os
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(
    title="AI Automation Python Service",
    description="Python compute and AI microservice engine for n8n workflows",
    version="1.0.0",
)


class LeadAnalysisRequest(BaseModel):
    name: str = Field(..., description="Lead contact name")
    email: str = Field(..., description="Lead email address")
    message: str = Field(..., description="Inquiry or message text")
    company: Optional[str] = Field(None, description="Company name if available")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary workflow context from n8n")


class LeadAnalysisResponse(BaseModel):
    status: str
    lead_name: str
    lead_email: str
    priority_score: int
    qualification: str
    sentiment: str
    tags: List[str]
    recommended_action: str


class TextProcessRequest(BaseModel):
    text: str
    action: str = Field(..., description="Action to perform: 'clean', 'extract_keywords', 'summary'")


@app.get("/health")
def health_check():
    """Health check endpoint to verify service connectivity from n8n or host."""
    return {
        "status": "healthy",
        "service": "ai-service",
        "version": "1.0.0",
    }


@app.post("/analyze-lead", response_model=LeadAnalysisResponse)
def analyze_lead(payload: LeadAnalysisRequest):
    """
    Simulates / runs intelligent lead qualification.
    Easily pluggable with OpenAI, LangChain, Anthropic, or local ML models.
    """
    message_lower = payload.message.lower()
    
    # Calculate priority based on keyword intent
    high_intent_keywords = ["pricing", "demo", "quote", "urgent", "enterprise", "schedule"]
    matches = [word for word in high_intent_keywords if word in message_lower]
    
    score = 50 + (len(matches) * 15)
    score = min(max(score, 10), 100)  # Bound between 10 and 100
    
    qualification = "high_intent" if score >= 80 else ("warm_lead" if score >= 50 else "low_intent")
    sentiment = "positive" if score >= 70 else ("neutral" if score >= 40 else "negative")
    
    action = (
        "Send VIP booking link & alert sales Slack channel"
        if qualification == "high_intent"
        else "Add to automated nurture email sequence"
    )
    
    return LeadAnalysisResponse(
        status="success",
        lead_name=payload.name,
        lead_email=payload.email,
        priority_score=score,
        qualification=qualification,
        sentiment=sentiment,
        tags=matches if matches else ["general_inquiry"],
        recommended_action=action,
    )


@app.post("/process-text")
def process_text(payload: TextProcessRequest):
    """Utility endpoint demonstrating string/data manipulation for n8n."""
    text = payload.text
    if payload.action == "clean":
        cleaned = " ".join(text.split())
        return {"original": text, "result": cleaned}
    elif payload.action == "extract_keywords":
        words = [w.strip(".,!?").lower() for w in text.split() if len(w) > 4]
        return {"keywords": list(set(words))}
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported action: {payload.action}")
