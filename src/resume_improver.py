def _has_content(value):
    """
    Check whether a resume section contains useful content.
    """

    if value is None:
        return False

    if not isinstance(value, str):
        return False

    return bool(value.strip())


def _get_text_length(value):
    """
    Return the number of characters in a section.
    """

    if not _has_content(value):
        return 0

    return len(value.strip())


def calculate_skill_keyword_coverage(
    resume_skills,
    job_skills
):
    """
    Calculate how many job-required skills
    are explicitly present in the resume.
    """

    resume_set = {
        str(skill).lower().strip()
        for skill in resume_skills
        if str(skill).strip()
    }

    job_set = {
        str(skill).lower().strip()
        for skill in job_skills
        if str(skill).strip()
    }

    matched_skills = sorted(
        resume_set.intersection(job_set)
    )

    missing_skills = sorted(
        job_set.difference(resume_set)
    )

    if not job_set:
        coverage = 0.0
    else:
        coverage = (
            len(matched_skills)
            / len(job_set)
        )

    return {
        "total_job_skills": len(job_set),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "coverage": coverage
    }


def calculate_resume_improvement_score(
    profile,
    skill_coverage
):
    """
    Calculate an explainable resume improvement score.

    This is a project-specific heuristic score.
    It is NOT an official ATS score.
    """

    score = 0.0

    # ------------------------------------------------
    # 1. Job skill coverage - 60 points
    # ------------------------------------------------

    skill_score = (
        skill_coverage["coverage"] * 60
    )

    score += skill_score

    # ------------------------------------------------
    # 2. Resume summary - 10 points
    # ------------------------------------------------

    summary = profile.get(
        "summary",
        ""
    )

    summary_length = _get_text_length(
        summary
    )

    if summary_length >= 80:
        score += 10

    elif summary_length >= 40:
        score += 7

    elif summary_length > 0:
        score += 4

    # ------------------------------------------------
    # 3. Projects - 10 points
    # ------------------------------------------------

    projects = profile.get(
        "projects",
        ""
    )

    if _has_content(projects):
        score += 10

    # ------------------------------------------------
    # 4. Education - 10 points
    # ------------------------------------------------

    education = profile.get(
        "education",
        ""
    )

    if _has_content(education):
        score += 10

    # ------------------------------------------------
    # 5. Experience - 5 points
    # ------------------------------------------------

    experience = profile.get(
        "experience",
        ""
    )

    if _has_content(experience):
        score += 5

    # ------------------------------------------------
    # 6. Additional evidence - 5 points
    # ------------------------------------------------

    additional_sections = [
        profile.get("certifications", ""),
        profile.get("achievements", ""),
        profile.get("publications", "")
    ]

    if any(
        _has_content(section)
        for section in additional_sections
    ):
        score += 5

    return round(
        min(score, 100.0),
        2
    )


def identify_resume_strengths(
    profile,
    skill_coverage
):
    """
    Identify positive aspects of the resume.
    """

    strengths = []

    coverage = skill_coverage["coverage"]

    # ------------------------------------------------
    # Skill coverage
    # ------------------------------------------------

    if coverage >= 0.80:
        strengths.append(
            "Strong coverage of the skills "
            "required by the target job."
        )

    elif coverage >= 0.60:
        strengths.append(
            "Good overlap between resume skills "
            "and the target job requirements."
        )

    elif coverage >= 0.40:
        strengths.append(
            "The resume contains some relevant "
            "skills for the target role."
        )

    # ------------------------------------------------
    # Summary
    # ------------------------------------------------

    summary = profile.get(
        "summary",
        ""
    )

    if _get_text_length(summary) >= 80:
        strengths.append(
            "The professional summary provides "
            "a reasonable amount of information."
        )

    # ------------------------------------------------
    # Projects
    # ------------------------------------------------

    if _has_content(
        profile.get("projects", "")
    ):
        strengths.append(
            "Projects are present and can provide "
            "evidence of practical technical skills."
        )

    # ------------------------------------------------
    # Education
    # ------------------------------------------------

    if _has_content(
        profile.get("education", "")
    ):
        strengths.append(
            "Education information is available."
        )

    # ------------------------------------------------
    # Experience
    # ------------------------------------------------

    if _has_content(
        profile.get("experience", "")
    ):
        strengths.append(
            "Experience information is available "
            "for evaluating practical exposure."
        )

    # ------------------------------------------------
    # Certifications
    # ------------------------------------------------

    if _has_content(
        profile.get("certifications", "")
    ):
        strengths.append(
            "Certifications or courses provide "
            "additional evidence of learning."
        )

    if not strengths:
        strengths.append(
            "The resume contains basic information, "
            "but more job-specific evidence could "
            "improve its strength."
        )

    return strengths


def identify_resume_weaknesses(
    profile,
    skill_coverage
):
    """
    Identify areas that could be improved.
    """

    weaknesses = []

    # ------------------------------------------------
    # Missing skills
    # ------------------------------------------------

    missing_skills = skill_coverage[
        "missing_skills"
    ]

    if missing_skills:
        weaknesses.append(
            "The resume does not explicitly mention "
            "some skills required by the target job."
        )

    # ------------------------------------------------
    # Summary
    # ------------------------------------------------

    summary = profile.get(
        "summary",
        ""
    )

    summary_length = _get_text_length(
        summary
    )

    if summary_length == 0:
        weaknesses.append(
            "No professional summary was detected."
        )

    elif summary_length < 40:
        weaknesses.append(
            "The professional summary is very short "
            "and could provide more role-specific context."
        )

    # ------------------------------------------------
    # Projects
    # ------------------------------------------------

    if not _has_content(
        profile.get("projects", "")
    ):
        weaknesses.append(
            "No project section was detected. "
            "If you have academic or personal projects, "
            "consider including them."
        )

    # ------------------------------------------------
    # Experience
    # ------------------------------------------------

    if not _has_content(
        profile.get("experience", "")
    ):
        weaknesses.append(
            "No experience section was detected. "
            "If you have internships, training, or work "
            "experience, consider including them."
        )

    # ------------------------------------------------
    # Skills
    # ------------------------------------------------

    if not profile.get("skills"):
        weaknesses.append(
            "No technical skills were detected "
            "from the resume."
        )

    return weaknesses


def generate_improvement_recommendations(
    profile,
    skill_coverage
):
    """
    Generate actionable recommendations.

    The system does not ask the candidate to
    fabricate skills or experience.
    """

    recommendations = []

    missing_skills = skill_coverage[
        "missing_skills"
    ]

    coverage = skill_coverage[
        "coverage"
    ]

    # ------------------------------------------------
    # Missing job skills
    # ------------------------------------------------

    if missing_skills:

        skills_text = ", ".join(
            skill.title()
            for skill in missing_skills
        )

        recommendations.append(
            "Review the missing job-relevant skills: "
            + skills_text
            + ". Add them to your resume only if "
            "you genuinely have experience or knowledge "
            "of those skills."
        )

    # ------------------------------------------------
    # Skill coverage
    # ------------------------------------------------

    if coverage < 0.50:

        recommendations.append(
            "The explicit skill coverage is below 50%. "
            "Consider developing relevant skills through "
            "projects, coursework, certifications, or "
            "practical experience."
        )

    elif coverage < 0.75:

        recommendations.append(
            "The skill coverage is moderate. "
            "Strengthening the missing relevant skills "
            "could improve your job alignment."
        )

    else:

        recommendations.append(
            "The resume already has strong explicit "
            "skill coverage for this job."
        )

    # ------------------------------------------------
    # Summary
    # ------------------------------------------------

    summary = profile.get(
        "summary",
        ""
    )

    if not _has_content(summary):

        recommendations.append(
            "Add a concise professional summary that "
            "highlights your technical background, "
            "relevant projects, and target role."
        )

    elif _get_text_length(summary) < 80:

        recommendations.append(
            "Expand the professional summary slightly "
            "to communicate your technical strengths "
            "and career direction."
        )

    # ------------------------------------------------
    # Projects
    # ------------------------------------------------

    if not _has_content(
        profile.get("projects", "")
    ):

        recommendations.append(
            "If you have academic or personal projects, "
            "include them and explain the technologies "
            "used and the problem solved."
        )

    else:

        recommendations.append(
            "Strengthen project descriptions by explaining "
            "your contribution, technologies used, and "
            "measurable outcomes when available."
        )

    # ------------------------------------------------
    # Experience
    # ------------------------------------------------

    if _has_content(
        profile.get("experience", "")
    ):

        recommendations.append(
            "Use clear action-oriented descriptions for "
            "experience and highlight relevant technical "
            "contributions."
        )

    # ------------------------------------------------
    # Skills organization
    # ------------------------------------------------

    if profile.get("skills"):

        recommendations.append(
            "Keep the technical skills section organized "
            "and prioritize skills that are genuinely "
            "relevant to the target role."
        )

    return recommendations


def analyze_resume_improvement(
    profile,
    job_profile
):
    """
    Main Resume Improvement Intelligence function.
    """

    resume_skills = profile.get(
        "skills",
        []
    )

    job_skills = job_profile.get(
        "skills",
        []
    )

    # ------------------------------------------------
    # Skill coverage
    # ------------------------------------------------

    skill_coverage = (
        calculate_skill_keyword_coverage(
            resume_skills,
            job_skills
        )
    )

    # ------------------------------------------------
    # Improvement score
    # ------------------------------------------------

    improvement_score = (
        calculate_resume_improvement_score(
            profile,
            skill_coverage
        )
    )

    # ------------------------------------------------
    # Strengths
    # ------------------------------------------------

    strengths = identify_resume_strengths(
        profile,
        skill_coverage
    )

    # ------------------------------------------------
    # Weaknesses
    # ------------------------------------------------

    weaknesses = identify_resume_weaknesses(
        profile,
        skill_coverage
    )

    # ------------------------------------------------
    # Recommendations
    # ------------------------------------------------

    recommendations = (
        generate_improvement_recommendations(
            profile,
            skill_coverage
        )
    )

    return {
        "improvement_score":
            improvement_score,

        "skill_coverage":
            skill_coverage,

        "strengths":
            strengths,

        "weaknesses":
            weaknesses,

        "recommendations":
            recommendations
    }