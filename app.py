def analyze_job_match(resume, job_description):
    resume_words = set(resume.lower().split())
    job_words = set(job_description.lower().split())

    matched_skills = resume_words.intersection(job_words)
    missing_words = job_words.difference(resume_words)

    return matched_skills, list(missing_words)[:10]


print("AI Career Assistant")
print("-------------------")

resume = input("Paste your resume text: ")
job_description = input("Paste the job description: ")

matched, missing = analyze_job_match(resume, job_description)

print("\nMatched Keywords:")
for word in matched:
    print("-", word)

print("\nPossible Missing Keywords:")
for word in missing:
    print("-", word)

print("\nSuggested Interview Questions:")
print("1. Tell me about your experience related to this role.")
print("2. What technical skills make you a good fit?")
print("3. Describe a project that matches this job description.")
