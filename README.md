# Yapma 🎯


## Basic Details
### Team Name: Delulu


### Team Members
- Member 1: Aisha Nama - Cusat
- Member 2: Anjana Sankar - Cusat
- Member 3: Majida Nasrin - Cusat

### Hosted Project Link
[mention your project hosted project link here]

### Project Description
YAPMA tackles the critical challenge of preventing harmful AI misuse by stopping unethical prompts at the source. We're shaping a safer, more responsible AI future—because it matters.

### The Problem statement
We're solving the absurd reality where people misuse AI to create harmful and unethical content—because honestly, who thought making AI a supervillian was a good idea? 😤 YAPMA steps in to say, "Not today, bestie!"

### The Solution
We’re giving AI a moral compass and a Gen Z vibe! 🌟 YAPMA sniffs out shady prompts, serves up sassy warnings, and stops harmful content before it even exists. Think of us as that loyal bestie your AI didn’t know it needed! 

## Technical Details
### Technologies/Components Used
For Software:
- Python 
- Streamlit, FastAPI
- Google-generativeai, Python-dotenv, Requests, Transformers
- Render

### Implementation
For Software:
# Installation
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload


streamlit run frontend\app.py

### Project Documentation
For Software:

# Screenshots 
![Screenshot1](https://i.imgur.com/f606Ljh.png)
*Home page of YAPMA*

![Screenshot2](https://i.imgur.com/EZaYORY.png)
*YAPMA dealing with unacceptable comments*

![Screenshot3](https://i.imgur.com/FTzOASf.png)
*YAPMA dealing with acceptable comments*

# Diagrams
![Workflow](https://i.imgur.com/knwvezq.png)
User inputs flow from Streamlit UI to FastAPI backend, where DistilBERT classifies prompts as Acceptable or Unacceptable, with GenZ feedback according to it.

### Project Demo
# Video
[https://drive.google.com/file/d/1cFuntqj6_IhYutVYxijsEt1OIjSstrj1/view?usp=sharing]
*The video demonstrates how YAPMA classifies the prompts as Acceptable and Unacceptablewith a certain confidence level.*


## Team Contributions
- Aisha Nama: Backend development, integrated pre-trained DistilBERT model for prompt moderation, version control.
- Anjana Sankar: Backend development, integrated Gemini API for GenZ feedback generation, handled hosting.
- Majida Nasrin: UI/UX design, Streamlit frontend development, created content and media for documentation.

---
Made with ❤️ by Delulu
