  import streamlit as st
import re
from collections import Counter

st.set_page_config(
    page_title="AI Career Assistant",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI Career Assistant")
st.write(
    "Analyze your resume against any job description, identify keyword gaps, "
    "and generate interview preparation suggestions."
)

st.divider()

resume = st.text_area("Paste Your Resume", height=260)
job_description = st.text_area("Paste Job Description", height=260)

stop_words = {
    "the", "and", "for", "with", "this", "that", "you", "your", "are", "will",
    "have", "has", "from", "our", "their", "they", "about", "into", "using",
    "use", "used", "able", "work", "role", "job", "team", "position",
    "responsibilities", "requirements", "experience", "skills", "ability",
    "including", "such", "across", "within", "based", "support", "strong",
    "good", "basic", "preferred", "required", "candidate", "company"
}

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9+#./ ]", " ", text)
    return text

def get_keywords(text, top_n=40):
    text = clean_text(text)
    words = text.split()

    keywords = []
    for word in words:
        if len(word) > 2 and word not in stop_words:
            keywords.append(word)

    keyword_counts = Counter(keywords)
    return [word for word, count in keyword_counts.most_common(top_n)]

def get_phrases(text):
    text = clean_text(text)

    phrase_patterns = [
        "data center", "machine learning", "artificial intelligence",
        "prompt engineering", "data analysis", "data visualization",
        "power bi", "project management", "technical documentation",
        "stakeholder communication", "network troubleshooting",
        "server hardware", "operating systems", "cloud computing",
        "ticketing systems", "cable management", "fiber optics",
        "structured cabling", "python programming", "sql queries",
        "business analysis", "quality assurance", "customer service"
    ]

    found = []
    for phrase in phrase_patterns:
        if phrase in text:
            found.append(phrase)

    return found

def create_interview_questions(matched, missing):
    questions = []

    if matched:
        for skill in matched[:3]:
            questions.append(f"Can you describe your experience with {skill}?")

    if missing:
        for skill in missing[:3]:
            questions.append(f"How would you start learning or gaining experience in {skill}?")

    questions.append("Tell me about a project where you solved a real problem.")
    questions.append("How do you explain technical information to a non-technical audience?")
    questions.append("What would you improve in one of your past projects?")

    return questions[:7]

if st.button("Analyze Resume Match"):
    if not resume.strip() or not job_description.strip():
        st.warning("Please paste both your resume and the job description.")
    else:
        resume_keywords = set(get_keywords(resume, 60))
        job_keywords = set(get_keywords(job_description, 60))

        resume_phrases = set(get_phrases(resume))
        job_phrases = set(get_phrases(job_description))

        matched_keywords = sorted(resume_keywords.intersection(job_keywords))
        missing_keywords = sorted(job_keywords.difference(resume_keywords))

        matched_phrases = sorted(resume_phrases.intersection(job_phrases))
        missing_phrases = sorted(job_phrases.difference(resume_phrases))

        total_job_terms = len(job_keywords) + len(job_phrases)
        total_matches = len(matched_keywords) + len(matched_phrases)

        if total_job_terms > 0:
            match_score = round((total_matches / total_job_terms) * 100)
        else:
            match_score = 0

        st.subheader("📊 Match Score")
        st.progress(min(match_score, 100) / 100)
        st.metric("Resume Match", f"{min(match_score, 100)}%")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matched Keywords & Skills")
            if matched_phrases or matched_keywords:
                for item in matched_phrases[:10]:
                    st.success(item.title())
                for item in matched_keywords[:20]:
                    st.success(item.title())
            else:
                st.info("No strong matches found.")

        with col2:
            st.subheader("⚠️ Missing Keywords & Skills")
            if missing_phrases or missing_keywords:
                for item in missing_phrases[:10]:
                    st.error(item.title())
                for item in missing_keywords[:20]:
                    st.error(item.title())
            else:
                st.success("No major missing keywords found.")

        st.subheader("📝 Resume Improvement Suggestions")
        if missing_phrases or missing_keywords:
            st.write("Consider strengthening your resume with relevant projects, coursework, or experience related to:")
            for item in (missing_phrases + missing_keywords)[:10]:
                st.write(f"- {item.title()}")
        else:
            st.write("Your resume appears to align well with the job description.")

        st.subheader("🎯 Suggested Interview Questions")
        questions = create_interview_questions(
            matched_phrases + matched_keywords,
            missing_phrases + missing_keywords
        )

        for i, question in enumerate(questions, 1):
            st.write(f"{i}. {question}")

        st.subheader("📧 Recruiter Message Draft")
        st.info(
            "Hi, I am interested in this role and believe my background aligns with the position. "
            "I have relevant experience and am excited about the opportunity to contribute. "
            "Please let me know the next steps."
        )

        st.subheader("🔍 Top Job Description Keywords")
        top_job_keywords = get_keywords(job_description, 25)
        st.write(", ".join(top_job_keywords))
