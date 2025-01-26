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
    "temperature": 1.5,  # Increase temperature for more randomness
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
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
        "- Be creative and generate completely random but contextually relevant messages.\n"
    )
)

def get_genz_message(label, prompt):
    # Define the instruction for generating messages based on the label
    instructions = {
        "Acceptable": f"The following prompt is classified as 'Acceptable'. Create a completely random but contextually relevant, Gen Z-styled positive comments for this prompt: '{prompt}'.",
        "Unacceptable": f"The following prompt is classified as 'Unacceptable'. Create a completely random but contextually relevant, Gen Z-styled warnings for this prompt: '{prompt}'."
    }


    try:
        # Generate the response using the appropriate instruction
        if label in instructions:
            logger.info(f"Generating Gemini response for label: {label}")
            logger.info(f"Prompt: {prompt}")
            response = model.generate_content(instructions[label])  # Use generate_content instead of generate_text
            logger.info(f"Full Gemini API Response: {response}")  # Log the full response

            if response and hasattr(response, "text"):
                # Log the response for debugging
                logger.info(f"Gemini API Response Text: {response.text}")
                return response.text.strip().split("\n")  # Split into individual messages
            else:
                logger.error("No text in the Gemini API response.")
                return None  # Return None if no text is generated
        else:
            logger.error(f"Invalid label provided: {label}")
            return None  # Return None for invalid labels
    except Exception as e:
        logger.error(f"Error generating GenZ message: {e}")
        return None  # Return None if an error occurs

def post_request_to_api(user_prompt):
    # Define the API URL
    API_URL = "https://yapma.onrender.com/classify"  

    # Prepare the request payload
    payload = {"prompt": user_prompt}

    try:
        # Send POST request
        response = requests.post(API_URL, json=payload)

        # Check if the response was successful
        if response.status_code == 200:
            return response.json()  # Assuming the API returns a JSON response
        else:
            logger.error(f"Failed to classify the prompt. Status code: {response.status_code}")
            return {"error": f"Failed to classify the prompt. Status code: {response.status_code}"}
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return {"error": f"Request failed: {str(e)}"}
