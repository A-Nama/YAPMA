from fastapi import FastAPI
from pydantic import BaseModel
from app.classifier import classify_prompt

app = FastAPI()

class PromptInput(BaseModel):
    prompt: str

@app.post("/classify")
def classify(input: PromptInput):
    result = classify_prompt(input.prompt)
    return result
