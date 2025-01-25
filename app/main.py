from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.classifier import classify_prompt
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class PromptInput(BaseModel):
    prompt: str

@app.post("/classify")
def classify(input: PromptInput):
    if not input.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    result = classify_prompt(input.prompt)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result

@app.get("/health")
def health_check():
    return {"status": "healthy"}