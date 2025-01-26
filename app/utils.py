import os
import google.generativeai as genai
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Generation configuration for the chatbot
generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "You are an empathetic, optimistic AI assistant specializing in ethical AI practices. Your role is to generate Gen Z-styled messages for classifying user prompts into categories: Acceptable and Unacceptable.\n\n"
        "Key guidelines:\n\n"
        "- For 'Acceptable' prompts, provide positive and encouraging messages that validate the appropriateness of the input.\n"
        "- For 'Unacceptable' prompts, create strong, clear rejections, emphasizing the need to avoid such inputs.\n"
        "- Maintain a casual, Gen Z tone with emojis and friendly language.\n"
    )
)

def get_genz_message(label):
    # Define the instruction for generating messages based on the label
    instructions = {
        "Acceptable": "Create two short, Gen Z-styled positive comments for an acceptable prompt.",
        "Unacceptable": "Create two short, Gen Z-styled warnings for a completely inappropriate or unacceptable prompt."
    }

    # Default messages for each label
    default_messages = {
        "Acceptable": ["✨ Go ahead, bestie! Your vibes are immaculate.", "All clear—keep being awesome!"],
        "Unacceptable": ["🚨 Stop right there! This is way out of bounds.", "🤢 Nope. This isn’t it, chief."]
    }

    try:
        # Generate the response using the appropriate instruction
        if label in instructions:
            response = model.generate_text(instructions[label])  # Generate text
            if response and hasattr(response, "text"):
                # Log the response for debugging
                logger.info(f"Gemini API Response: {response.text}")
                return response.text.strip().split("\n")  # Split into individual messages
            else:
                logger.error("No text in the Gemini API response.")
                return default_messages[label]
        else:
            logger.error("Invalid label provided.")
            return default_messages.get(label, ["🤔 Something went wrong with label!"])
    except Exception as e:
        logger.error(f"Error generating GenZ message: {e}")
        return default_messages.get(label, ["🤔 Something went wrong with message!"])

def post_request_to_api(user_prompt):
    # Define the API URL
    API_URL = "http://127.0.0.1:8000/classify"  # Replace with your actual API URL if hosted elsewhere

    # Prepare the request payload
    payload = {"prompt": user_prompt}

    try:
        # Send POST request
        response = requests.post(API_URL, json=payload)

        # Check if the response was successful
        if response.status_code == 200:
            return response.json()  # Return the JSON response
        else:
            logger.error(f"Failed to classify the prompt. Status code: {response.status_code}")
            return {"error": f"Failed to classify the prompt. Status code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return {"error": f"Request failed: {str(e)}"}