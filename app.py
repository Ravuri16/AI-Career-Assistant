import streamlit as st

st.title("AI Career Assistant")

st.write("Analyze your resume against a job description.")

resume = st.text_area("Paste your Resume")

job_description = st.text_area("Paste Job Description")

if st.button("Analyze"):

    resume_words = set(resume.lower().split())
    job_words = set(job_description.lower().split())

    matched = resume_words.intersection(job_words)
    missing = job_words.difference(resume_words)

    st.subheader("Matched Skills")
    for skill in matched:
        st.write(f"✅ {skill}")

    st.subheader("Missing Skills")
    for skill in list(missing)[:10]:
        st.write(f"❌ {skill}")

    st.subheader("Suggested Interview Questions")
    st.write("1. Tell me about a project related to this role.")
    st.write("2. What technical skills make you a good fit?")
    st.write("3. Describe a challenge you solved.")
