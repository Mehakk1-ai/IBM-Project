import pandas as pd

def recommend_courses(missing_skills):
    course_df = pd.read_csv("Data\course_catalog.csv")
    recommendations = {}
    
    for skill in missing_skills:
        match = course_df[course_df["skill"] == skill]
        if not match.empty:
            recommendations[skill] = match.iloc[0]["course_link"]
    
    return recommendations
