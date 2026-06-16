import streamlit as st
import re

st.set_page_config(page_title="AI Career Assistant", page_icon="💼", layout="wide")

st.title("💼 AI Career Assistant")
st.write(
    "Compare your resume with a job description and receive a match score, "
    "skill gaps, resume suggestions, and interview preparation questions."
)

st.divider()

resume = st.text_area("Paste Your Resume", height=250)
job_description = st.text_area("Paste Job Description", height=250)

skill_library = {
    "Data & Analytics": [
        "python", "sql", "excel", "tableau", "power bi", "data analysis",
        "data visualization", "dashboard", "reporting", "pandas", "numpy",
        "machine learning", "statistics", "etl", "data quality"
    ],
    "Software & Cloud": [
        "java", "javascript", "html", "css", "react", "angular", "api",
        "rest api", "git", "github", "aws", "azure", "gcp", "docker",
        "kubernetes", "linux", "streamlit"
    ],
    "Finance": [
        "finance", "accounting", "economics", "financial modeling",
        "capital markets", "corporate financial reporting", "restructuring",
        "distressed investing", "leveraged finance", "private placements",
        "credit", "valuation", "powerpoint", "excel"
    ],
    "Data Center & IT": [
        "tcp/ip", "networking", "server", "hardware", "data center",
        "cabling", "fiber optics", "structured cabling", "operating systems",
        "troubleshooting", "ticketing", "remote hands", "security",
        "power", "cooling"
    ],
    "Professional Skills": [
        "communication", "documentation", "stakeholder", "teamwork",
        "leadership", "problem solving", "attention to detail",
        "writing", "presentation", "agile", "jira"
    ],
    "AI Skills": [
        "ai", "artificial intelligence", "claude", "chatgpt",
        "prompt engineering", "automation", "llm", "generative ai"
    ]
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9+#./ ]", " ", text)
    return text

def find_skills(text):
    text = clean_text(text)
    found = {}

    for category, skills in skill_library.items():
        matched = []
        for skill in skills:
            if skill in text:
                matched.append(skill)
        if matched:
            found[category] = sorted(set(matched))

    return found

def flatten_skills(skill_dict):
    all_skills = []
    for skills in skill_dict.values():
        all_skills.extend(skills)
    return set(all_skills)

if st.button("Analyze Resume Match"):
    if not resume.strip() or not job_description.strip():
        st.warning("Please paste both your resume and the job description.")
    else:
        resume_skill_dict = find_skills(resume)
        job_skill_dict = find_skills(job_description)

        resume_skills = flatten_skills(resume_skill_dict)
        job_skills = flatten_skills(job_skill_dict)

        matched_skills = sorted(resume_skills.intersection(job_skills))
        missing_skills = sorted(job_skills.difference(resume_skills))

        if job_skills:
            match_score = round((len(matched_skills) / len(job_skills)) * 100)
        else:
            match_score = 0

        st.subheader("📊 Match Score")
        st.progress(match_score / 100)
        st.metric("Resume Match", f"{match_score}%")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matched Skills")
            if matched_skills:
                for skill in matched_skills:
                    st.success(skill.title())
            else:
                st.info("No matching skills found.")

        with col2:
            st.subheader("⚠️ Missing Skills")
            if missing_skills:
                for skill in missing_skills:
                    st.error(skill.title())
            else:
                st.success("No major missing skills found.")

        st.subheader("📌 Skills Found in Job Description")
        if job_skill_dict:
            for category, skills in job_skill_dict.items():
                st.write(f"**{category}:** {', '.join([s.title() for s in skills])}")
        else:
            st.write("No recognized skills found in the job description.")

        st.subheader("📝 Resume Improvement Suggestions")
        if missing_skills:
            st.write("Consider adding relevant projects, coursework, certifications, or experience related to:")
            for skill in missing_skills[:10]:
                st.write(f"- {skill.title()}")
        else:
            st.write("Your resume includes the main skills detected in the job description.")

        st.subheader("🎯 Suggested Interview Questions")
        focus_skills = missing_skills[:4] if missing_skills else matched_skills[:4]

        if focus_skills:
            for i, skill in enumerate(focus_skills, 1):
                st.write(f"{i}. Can you describe your experience or learning plan for {skill.title()}?")
            st.write(f"{len(focus_skills)+1}. Tell me about a project where you solved a real problem.")
            st.write(f"{len(focus_skills)+2}. How do you explain technical information to non-technical stakeholders?")
        else:
            st.write("1. Tell me about your background and why you are interested in this role.")
            st.write("2. Describe a project you built from start to finish.")
            st.write("3. What skills are you currently improving?")

        st.subheader("📧 Recruiter Message Draft")
        st.info(
            "Hi, I am interested in this role and believe my background aligns with the position. "
            "I have relevant experience and am excited about the opportunity to contribute. "
            "Please let me know the next steps."
        )
