import streamlit as st
import requests

# Backend API URL
API_URL = "http://127.0.0.1:8000/classify"

st.title("YAPMA: Your AI Prompt Moderation Assistant 🎭")

# Input prompt from user
user_prompt = st.text_area("Enter your prompt here:")

if st.button("Moderate Prompt"):
    if user_prompt.strip():
        # Send request to the backend
        response = requests.post(API_URL, json={"prompt": user_prompt})
        if response.status_code == 200:
            data = response.json()
            if "label" in data:
                st.markdown(f"### Classification: **{data['label']}**")
                st.markdown(f"**Confidence:** {data['confidence']:.2f}")

                # Display GenZ messages
                genz_messages = data.get("genz_message", ["✨ Keep it ethical, bestie!"])
                for message in genz_messages:
                    st.success(message)
            else:
                st.error(data.get("error", "An error occurred!"))
        else:
            st.error("Failed to connect to the backend.")
    else:
        st.warning("Please enter a prompt!")

# Add footer
st.markdown("---")
st.markdown("🚀 Built with ❤️ by Team YAPMA")