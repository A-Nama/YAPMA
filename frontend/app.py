import streamlit as st
import requests

# Backend API URL
API_URL = "http://127.0.0.1:8000/classify"

# Add custom CSS for styling
page_bg_css = """
<style>
/* General font styling for the entire app */
* {
    font-family: 'Playfair Display', serif;  /* Apply Playfair Display font globally */
}

/* General app background */
[data-testid="stAppViewContainer"] {
    background-color: #e4e2dd;  /* Light gray background */
    padding: -100px;  /* Add padding around the app */
}

/* Center-align the main container */
[data-testid="stVerticalBlock"] {
    align-items: center;
    justify-content: center;
}

/* Initial animation (only runs when page loads) */
.logo-container img {
    animation: initialAnimation 2s ease-out forwards;  /* Initial animation */
    transform-origin: center;
}

/* Keyframes for the initial animation */
@keyframes initialAnimation {
    0% { transform: scale(0.8); opacity: 0; }      /* Start smaller and invisible */
    50% { transform: scale(1.1); opacity: 1; }     /* Scale up and become visible */
    100% { transform: scale(1); opacity: 1; }      /* Final normal size */
}

/* Hover animation (activates when the mouse hovers over the logo) */
.logo-container img:hover {
    animation: hoverAnimation 0.5s ease-out forwards;  /* Hover effect */
}

/* Keyframes for the hover animation */
@keyframes hoverAnimation {
    0% { transform: scale(1); }         /* Normal size */
    50% { transform: scale(1.2); }      /* Scale up */
    100% { transform: scale(1); }       /* Return to normal size */
}

/* Change the font and color for "Enter your prompt here" */
h3 {
    color: black !important;  /* Set the color to black */
    font-size: 24px;  /* Set font size */
    font-family: 'Playfair Display', serif;  /* Apply custom font specifically here */
}

/* Adjust the logo */
.logo-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: -180px;
}

/* Stylish text area box design (without gradient) */
div.stTextArea textarea {
    color: black !important;  /* Text color inside textarea */
    background-color: #f2f2f2 !important;  /* Light gray background (solid color) */
    border: 2px solid #ccc !important;  /* Soft border */
    padding: 20px;  /* Add padding for better spacing */
    border-radius: 12px;  /* Rounded corners */
    font-size: 18px;  /* Font size inside the text area */
    font-family: 'Playfair Display', serif;  /* Apply custom font */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);  /* Subtle shadow */
    width: 80%;  /* Set width of the text area */
    margin: 20px auto;  /* Center-align the text area */
    transition: all 0.3s ease-in-out;  /* Smooth transition for hover/focus effects */
}

/* Add hover effect on text area */
div.stTextArea textarea:hover {
    transform: scale(1.05);  /* Slightly enlarge the text area when hovered */
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);  /* Add more shadow on hover */
}

/* Focus effect */
div.stTextArea textarea:focus {
    background-color: #e0e0e0 !important;  /* Lighter gray background on focus */
    outline: none;  /* Remove the default outline */
    border-radius: 12px;  /* Keep the rounded corners */
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.3);  /* Stronger shadow on focus */
}

/* Placeholder styling */
div.stTextArea textarea::placeholder {
    color: #245698 !important;  /* Black placeholder text */
    font-style: italic;  /* Italicize placeholder text */
}

/* Button alignment */
div.stButton button {
    width: 200px;  /* Set button width */
    margin: 20px auto;  /* Center-align button */
    display: block;
}

/* Importing Playfair Display font from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&display=swap');
</style>
"""
st.markdown(page_bg_css, unsafe_allow_html=True)

# Logo section
logo_url = "https://i.imgur.com/TG4wo53.png"
st.markdown(
    f"""
    <div class="logo-container">
        <img src="{logo_url}" alt="Logo" width="300">
    </div>
    """,
    unsafe_allow_html=True,
)

# Input prompt section
st.markdown("<h3 style='text-align: center;'>Enter your prompt here:</h3>", unsafe_allow_html=True)
user_prompt = st.text_area("", height=200, key="user_prompt")

# "Moderate Prompt" button
if st.button("Moderate Prompt"):
    if user_prompt.strip():
        # Send request to the backend
        response = requests.post(API_URL, json={"prompt": user_prompt})
        if response.status_code == 200:
            data = response.json()
            if "label" in data:
                st.markdown(f"<h4 style='text-align: center;'>Classification: <b>{data['label']}</b></h4>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='text-align: center;'>Confidence: {data['confidence']:.2f}</h4>", unsafe_allow_html=True)

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
