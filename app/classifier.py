from transformers import pipeline

# Load pre-trained DistilBERT Toxic Comment Classifier
MODEL_NAME = "unitary/toxic-bert"
classifier = pipeline("text-classification", model=MODEL_NAME)

label_mapping = {0: "Acceptable", 1: "Shady", 2: "Unacceptable"}

def classify_prompt(prompt):
    try:
        result = classifier(prompt)
        label_id = int(result[0]["label"].split("_")[-1])  # Extract label ID
        label = label_mapping.get(label_id, "Unknown")
        confidence = result[0]["score"]
        return {"label": label, "confidence": confidence}
    except Exception as e:
        return {"error": str(e)}
