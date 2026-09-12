from src.job_analyzer import (
    analyze_job_description
)

from src.matcher import (
    calculate_semantic_similarity,
    calculate_skill_match,
    calculate_overall_score
)


def match_resume_to_job(
    resume_text,
    resume_skills,
    resume_embedding,
    job_description,
    skills_df,
    embedding_model
):
    """
    Compare one resume against one job.

    The resume embedding is supplied so that
    it does not need to be recalculated.
    """

    # -----------------------------------------
    # JOB ANALYSIS
    # -----------------------------------------

    job_profile = analyze_job_description(
        job_description,
        skills_df
    )

    # -----------------------------------------
    # SKILL MATCHING
    # -----------------------------------------

    skill_result = calculate_skill_match(
        resume_skills,
        job_profile["skills"]
    )

    # -----------------------------------------
    # JOB EMBEDDING
    # -----------------------------------------

    job_embedding = (
        embedding_model.encode(
            job_description
        )
    )

    # -----------------------------------------
    # SEMANTIC SIMILARITY
    # -----------------------------------------

    semantic_score = (
        calculate_semantic_similarity(
            resume_embedding,
            job_embedding
        )
    )

    # -----------------------------------------
    # OVERALL SCORE
    # -----------------------------------------

    overall_score = (
        calculate_overall_score(
            semantic_score,
            skill_result["skill_score"]
        )
    )

    return {

        "job_description":
            job_description,

        "job_profile":
            job_profile,

        "semantic_score":
            semantic_score,

        "skill_score":
            skill_result["skill_score"],

        "overall_score":
            overall_score,

        "matched_skills":
            skill_result["matched_skills"],

        "missing_skills":
            skill_result["missing_skills"],

        "additional_skills":
            skill_result["additional_skills"]
    }


def rank_jobs(
    resume_text,
    resume_skills,
    jobs,
    skills_df,
    embedding_model
):
    """
    Rank multiple jobs according to
    resume-job compatibility.
    """

    results = []

    # -----------------------------------------
    # Calculate resume embedding ONCE
    # -----------------------------------------

    resume_embedding = (
        embedding_model.encode(
            resume_text
        )
    )

    # -----------------------------------------
    # Process every job
    # -----------------------------------------

    for job in jobs:

        title = job.get(
            "title",
            "Untitled Job"
        )

        description = job.get(
            "description",
            ""
        )

        if not description.strip():
            continue

        result = match_resume_to_job(
            resume_text,
            resume_skills,
            resume_embedding,
            description,
            skills_df,
            embedding_model
        )

        result["title"] = title

        results.append(
            result
        )

    # -----------------------------------------
    # Rank jobs
    # -----------------------------------------

    results.sort(
        key=lambda item:
            item["overall_score"],
        reverse=True
    )

    # -----------------------------------------
    # Assign ranking
    # -----------------------------------------

    for index, result in enumerate(
        results,
        start=1
    ):

        result["rank"] = index

    return results