from src.skill_extractor import (
    extract_skills,
    group_skills_by_category
)


def analyze_job_description(
    job_description,
    skills_df
):
    """
    Analyze a job description and create
    a structured job profile.
    """

    skills = extract_skills(
        job_description,
        skills_df
    )

    skill_categories = (
        group_skills_by_category(
            skills,
            skills_df
        )
    )

    job_profile = {

        "description":
            job_description,

        "skills":
            skills,

        "skill_categories":
            skill_categories,

        "skill_count":
            len(skills)
    }

    return job_profile