from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.classifier import classify_prompt
from app.utils import get_genz_message  # Import the Gemini message generator
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

    # Classify the prompt
    classification_result = classify_prompt(input.prompt)
    if "error" in classification_result:
        raise HTTPException(status_code=500, detail=classification_result["error"])

    # Generate Gen Z-styled message using the classification label and the actual prompt
    genz_message = get_genz_message(classification_result["label"], input.prompt)

    # Handle the case where genz_message is None
    if genz_message is None:
        raise HTTPException(status_code=500, detail="Failed to generate Gen Z messages.")

    # Prepare the response to include the label, confidence, and the generated message
    response = {
        "label": classification_result["label"],
        "confidence": classification_result["confidence"],
        "genz_message": genz_message,  # AI-generated messages
    }

    return response

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=PORT)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")