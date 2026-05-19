import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader

# Configure Gemini API
genai.configure(api_key="GEMINI_API_KEY")

# Load Gemini model
model = genai.GenerativeModel("models/gemini-2.5-flash")

# App title
st.title("📄 AI Career Copilot")
st.write("Upload your resume, paste a job description, and get AI-powered career insights.")

# Upload resume
uploaded_file = st.file_uploader("📂 Upload Resume PDF", type="pdf")

# Job description input box
job_description = st.text_area(
    "📋 Copy & Paste Job Description Here",
    height=250
)

resume_text = ""

if uploaded_file:
    # Read PDF
    pdf = PdfReader(uploaded_file)

    for page in pdf.pages:
        resume_text += page.extract_text()

    st.success("✅ Resume uploaded successfully!")

    # Dropdown menu
    option = st.selectbox(
        "Choose an option",
        [
            "Ask Resume Question",
            "Ask Resume + Job Description Question",
            "Resume vs Job Match",
            "Generate Interview Questions"
        ]
    )

    # OPTION 1: Ask about resume only
    if option == "Ask Resume Question":
        question = st.text_input("❓ Ask a question about the resume:")

        if question:
            prompt = f"""
            Resume:
            {resume_text}

            Question:
            {question}
            """

            response = model.generate_content(prompt)
            st.write(response.text)

    # OPTION 2: Ask anything about resume + JD
    elif option == "Ask Resume + Job Description Question":
        question = st.text_input(
            "❓ Ask anything about resume and job description:"
        )

        if question:
            if job_description:
                prompt = f"""
                Resume:
                {resume_text}

                Job Description:
                {job_description}

                Question:
                {question}
                """

                response = model.generate_content(prompt)
                st.write(response.text)
            else:
                st.warning("⚠️ Please paste a job description first.")

    # OPTION 3: Match score
    elif option == "Resume vs Job Match":
        if st.button("Check Match Score"):
            if job_description:
                prompt = f"""
                Compare this resume with the following job description.

                Resume:
                {resume_text}

                Job Description:
                {job_description}

                Give:
                1. Match score out of 100
                2. Missing skills
                3. Suggestions to improve
                """

                response = model.generate_content(prompt)
                st.write(response.text)
            else:
                st.warning("⚠️ Please paste a job description first.")

    # OPTION 4: Interview questions
    elif option == "Generate Interview Questions":
        if st.button("Generate Questions"):
            if job_description:
                prompt = f"""
                Based on this resume and job description,
                generate 10 likely interview questions.

                Resume:
                {resume_text}

                Job Description:
                {job_description}
                """

                response = model.generate_content(prompt)
                st.write(response.text)
            else:
                st.warning("⚠️ Please paste a job description first.")