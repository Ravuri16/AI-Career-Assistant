import streamlit as st
import re

st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI Career Assistant")
st.write(
    "Analyze your resume against a job description, identify skill gaps, "
    "and prepare for interviews more effectively."
)

st.divider()

resume = st.text_area("Paste Your Resume", height=250)
job_description = st.text_area("Paste Job Description", height=250)

common_skills = [
    "python", "sql", "tableau", "power bi", "excel", "java", "javascript",
    "aws", "azure", "gcp", "machine learning", "data analysis", "pandas",
    "numpy", "spark", "kafka", "airflow", "git", "jira", "linux",
    "networking", "cloud", "docker", "kubernetes", "streamlit"
]

def clean_text(text):
    return re.sub(r"[^a-zA-Z0-9+#. ]", " ", text.lower())

def find_skills(text):
    text = clean_text(text)
    return [skill for skill in common_skills if skill in text]

if st.button("Analyze Resume Match"):
    if not resume or not job_description:
        st.warning("Please paste both your resume and the job description.")
    else:
        resume_skills = set(find_skills(resume))
        job_skills = set(find_skills(job_description))

        matched_skills = sorted(resume_skills.intersection(job_skills))
        missing_skills = sorted(job_skills.difference(resume_skills))

        if job_skills:
            match_score = round((len(matched_skills) / len(job_skills)) * 100)
        else:
            match_score = 0

        st.subheader("Match Score")
        st.progress(match_score / 100)
        st.metric("Resume Match", f"{match_score}%")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Matched Skills")
            if matched_skills:
                for skill in matched_skills:
                    st.success(skill.title())
            else:
                st.info("No matching skills found.")

        with col2:
            st.subheader("Missing Skills")
            if missing_skills:
                for skill in missing_skills:
                    st.error(skill.title())
            else:
                st.success("No major missing skills found.")

        st.subheader("Resume Improvement Suggestions")
        if missing_skills:
            st.write("Consider adding relevant experience, coursework, or projects related to:")
            for skill in missing_skills:
                st.write(f"- {skill.title()}")
        else:
            st.write("Your resume already includes the key skills found in the job description.")

        st.subheader("Suggested Interview Questions")
        st.write("1. Tell me about a project where you used the key skills required for this role.")
        st.write("2. How have you solved a technical or data-related problem?")
        st.write("3. How do you communicate technical information to non-technical stakeholders?")
        st.write("4. What would you improve in one of your past projects?")

        st.subheader("Recruiter Message Draft")
        st.info(
            "Hi, I am interested in this role and believe my background aligns well "
            "with the requirements. I have experience with relevant technical skills "
            "and would appreciate the opportunity to discuss how I can contribute. "
            "Please let me know the next steps."
        )
