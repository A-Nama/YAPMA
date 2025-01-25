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
    # Add other possible labels returned by the model
}

# Define a threshold for confidence to classify as "Shady"
CONFIDENCE_THRESHOLD = 0.5

def classify_prompt(prompt):
    try:
        # Step 1: Validate the input prompt
        if not prompt or not isinstance(prompt, str):
            raise ValueError("Invalid input: Prompt must be a non-empty string.")

        # Step 2: Classify the input prompt
        try:
            results = classifier(prompt)
            print("Raw model output:", results)  # Log the raw output
        except Exception as e:
            raise RuntimeError(f"Error during model inference: {e}")

        # Step 3: Initialize variables to store the final label and confidence
        final_label = "Acceptable"
        final_confidence = 1.0

        # Step 4: Iterate through all results to find the most relevant label
        try:
            for result in results:
                model_label = result["label"]
                confidence = result["score"]
                print(f"Model label: {model_label}, Confidence: {confidence}")  # Log each result

                # Step 5: Map model label to custom label
                try:
                    custom_label = label_mapping.get(model_label, "Shady")
                except Exception as e:
                    raise KeyError(f"Error mapping model label '{model_label}': {e}")

                # Step 6: Update final label and confidence if the current result is more relevant
                if confidence > final_confidence:
                    final_label = custom_label
                    final_confidence = confidence

            # Step 7: If confidence is low, classify as "Shady"
            if final_confidence < CONFIDENCE_THRESHOLD:
                final_label = "Shady"

        except Exception as e:
            raise RuntimeError(f"Error processing model results: {e}")

        # Step 8: Return the final classification
        return {"label": final_label, "confidence": final_confidence}

    except ValueError as ve:
        logger.error(f"Validation error: {ve}")
        return {"error": str(ve)}
    except KeyError as ke:
        logger.error(f"Key error: {ke}")
        return {"error": str(ke)}
    except RuntimeError as re:
        logger.error(f"Runtime error: {re}")
        return {"error": str(re)}
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"error": str(e)}