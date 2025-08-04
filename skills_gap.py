def compare_skills(user_skills, job_skills):
    user_set = set(user_skills)
    job_set = set(job_skills)
    
    return {
        "existing": list(user_set & job_set),         # common skills
        "missing": list(job_set - user_set)           # what you're lacking
    }
