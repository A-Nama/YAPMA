from transformers import pipeline

# Load pre-trained DistilBERT Toxic Comment Classifier
MODEL_NAME = "unitary/toxic-bert"
classifier = pipeline("text-classification", model=MODEL_NAME)

# Map model labels to custom labels
label_mapping = {
    "toxic": "Unacceptable",
    "non-toxic": "Acceptable"
}

def classify_prompt(prompt):
    try:
        # Classify the input prompt
        result = classifier(prompt)

        # Extract label and confidence
        if result:
            model_label = result[0]["label"]  # Model label (e.g., "toxic", "non-toxic")
            confidence = result[0]["score"]  # Confidence score
            
            # Map model label to custom label
            custom_label = label_mapping.get(model_label, "Shady")
        else:
            # Handle cases where no label is returned
            custom_label = "Acceptable"
            confidence = 1.0  # Assume full confidence for acceptable prompts

        return {"label": custom_label, "confidence": confidence}
    except Exception as e:
        return {"error": str(e)}
