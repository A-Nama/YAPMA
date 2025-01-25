from transformers import pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load pre-trained DistilBERT Toxic Comment Classifier
MODEL_NAME = "unitary/toxic-bert"
classifier = pipeline("text-classification", model=MODEL_NAME)

# Map model labels to custom labels
label_mapping = {
    "toxic": "Unacceptable",
    "non-toxic": "Acceptable",
}


def classify_prompt(prompt):
    try:
        # Classify the input prompt
        results = classifier(prompt)
        print("Raw model output:", results)  # Log the raw output

        # Initialize variables to store the final label and confidence
        final_label = "Acceptable"
        final_confidence = 0.0

        # Iterate through all results to find the most relevant label
        for result in results:
            model_label = result["label"]
            confidence = result["score"]
            print(f"Model label: {model_label}, Confidence: {confidence}")  # Log each result

            # If the label is "toxic" and confidence is high, classify as "Unacceptable"
            if model_label == "toxic" and confidence > 0.5:  # Adjust threshold as needed
                final_label = "Unacceptable"
                final_confidence = confidence
                break  # Stop iterating once we find a high-confidence "toxic" label

        return {"label": final_label, "confidence": final_confidence}

    except Exception as e:
        logger.error(f"Error classifying prompt: {e}")
        return {"error": str(e)}