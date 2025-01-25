from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from classifier import classify_prompt
import logging
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Read port from environment, with a fallback to 8000
PORT = int(os.getenv("PORT", 8000))


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yapma-1.onrender.com"],  # Allows all origins, adjust as needed for security
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
