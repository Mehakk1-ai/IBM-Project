"""import spacy

nlp = spacy.load("en_core_web_sm")

def extract_skills(text, skill_list):
    text = text.lower()
    doc = nlp(text)
    tokens = [token.text for token in doc]
    matched_skills = set()
    for skill in skill_list:
        if skill in tokens or skill in text:
            matched_skills.add(skill)
    return matched_skills"""


import re

def extract_skills(resume_text, skill_list):
    resume_text = resume_text.lower()
    found_skills = set()
    for skill in skill_list:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, resume_text):
            found_skills.add(skill)
    return list(found_skills)
