import os
import streamlit as st
import pandas as pd
import fitz  # PyMuPDF

# Import your custom functions
from Scripts.skills import extract_skills
from Scripts.skills_gap import compare_skills
from Scripts.recommend_courses import recommend_courses

@st.cache_data
def load_skill_data():
    skill_df = pd.read_csv("Data/skill_db.csv")
    return skill_df["skill"].tolist()

@st.cache_data
def load_job_data():
    return pd.read_csv("Data/jobroles.csv")

skill_list = load_skill_data()
job_df = load_job_data()


st.set_page_config(page_title="Skill Gap Analyzer", layout="centered")
st.title("🧠 AI Skill Gap Analyzer")

st.markdown("Upload your resume or paste its text, and we'll compare it with your target job's skill requirements.")


uploaded_file = st.file_uploader("📄 Upload your resume (PDF only):", type=["pdf"])

# Session state to store resume text
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if uploaded_file and uploaded_file.name.endswith(".pdf"):
    with st.spinner("🔍 Extracting text from resume..."):
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            st.session_state.resume_text = text


selected_job = st.selectbox("💼 Select a job role to compare against:", job_df['job_title'].unique())

if st.button("🔍 Analyze Skill Gap"):
    resume_text = st.session_state.resume_text.strip()

    if not resume_text:
        st.warning(" Please upload a resume.")
    else:
        with st.spinner("Analyzing skills..."):
            # Step 1: Extract skills from resume
            user_skills = extract_skills(resume_text, skill_list)

            # Step 2: Get job skills
            job_skills = job_df[job_df['job_title'] == selected_job].iloc[0]['skills'].split(',')

            # Step 3: Compare skills
            result = compare_skills(user_skills, job_skills)

           
            st.subheader(" Skills You Already Have")
            st.write(result["existing"] if result["existing"] else "No matches found.")

            st.subheader(" Missing Skills for This Role")
            st.write(result["missing"] if result["missing"] else "You're all set!")

            
            st.subheader(" Suggested Courses")
            recommendations = recommend_courses(result["missing"])

            if recommendations:
                for skill, link in recommendations.items():
                    st.markdown(f"- [{skill.capitalize()}]({link})")
            else:
                st.info("No course suggestions found for missing skills.")

