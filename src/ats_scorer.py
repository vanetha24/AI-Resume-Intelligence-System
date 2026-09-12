# ============================================================
# ATS SCORER
# ============================================================

from src.matcher import (
    calculate_semantic_similarity,
    calculate_skill_match
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _has_content(value):
    """
    Check whether a value contains meaningful text.
    """

    if value is None:
        return False

    if not isinstance(value, str):
        return False

    return bool(value.strip())


def _safe_score(value):
    """
    Keep a score between 0 and 1.
    """

    try:

        value = float(value)

    except (TypeError, ValueError):

        return 0.0

    return max(
        0.0,
        min(
            1.0,
            value
        )
    )


# ============================================================
# KEYWORD MATCH SCORE
# ============================================================

def calculate_keyword_score(
    resume_skills,
    job_skills
):
    """
    Calculate ATS-style keyword/skill matching.

    Returns a value between 0 and 1.
    """

    skill_result = calculate_skill_match(
        resume_skills,
        job_skills
    )

    return {
        "score": _safe_score(
            skill_result["skill_score"]
        ),

        "matched_skills":
            skill_result["matched_skills"],

        "missing_skills":
            skill_result["missing_skills"],

        "additional_skills":
            skill_result["additional_skills"]
    }


# ============================================================
# SECTION COMPLETENESS
# ============================================================

def calculate_section_completeness(
    resume_profile
):
    """
    Evaluate important resume sections.

    Maximum score = 1.0
    """

    sections = {
        "summary": 0.20,
        "skills": 0.20,
        "education": 0.20,
        "experience": 0.20,
        "projects": 0.20
    }

    score = 0.0

    present_sections = []
    missing_sections = []

    for section, weight in sections.items():

        value = resume_profile.get(
            section
        )

        if section == "skills":

            if value:

                score += weight

                present_sections.append(
                    section
                )

            else:

                missing_sections.append(
                    section
                )

        else:

            if _has_content(value):

                score += weight

                present_sections.append(
                    section
                )

            else:

                missing_sections.append(
                    section
                )

    return {
        "score": _safe_score(score),
        "present_sections": present_sections,
        "missing_sections": missing_sections
    }


# ============================================================
# EXPERIENCE RELEVANCE
# ============================================================

def calculate_experience_relevance(
    resume_profile,
    job_description,
    embedding_model
):
    """
    Compare resume experience against job description.
    """

    experience = resume_profile.get(
        "experience",
        ""
    )

    if not _has_content(experience):

        return {
            "score": 0.0,
            "available": False
        }

    experience_embedding = (
        embedding_model.encode(
            experience
        )
    )

    job_embedding = (
        embedding_model.encode(
            job_description
        )
    )

    similarity = calculate_semantic_similarity(
        experience_embedding,
        job_embedding
    )

    return {
        "score": _safe_score(similarity),
        "available": True
    }


# ============================================================
# PROJECT RELEVANCE
# ============================================================

def calculate_project_relevance(
    resume_profile,
    job_description,
    embedding_model
):
    """
    Compare resume projects against job description.
    """

    projects = resume_profile.get(
        "projects",
        ""
    )

    if not _has_content(projects):

        return {
            "score": 0.0,
            "available": False
        }

    project_embedding = (
        embedding_model.encode(
            projects
        )
    )

    job_embedding = (
        embedding_model.encode(
            job_description
        )
    )

    similarity = calculate_semantic_similarity(
        project_embedding,
        job_embedding
    )

    return {
        "score": _safe_score(similarity),
        "available": True
    }


# ============================================================
# EDUCATION RELEVANCE
# ============================================================

def calculate_education_score(
    resume_profile
):
    """
    Check whether education information exists.
    """

    education = resume_profile.get(
        "education",
        ""
    )

    if _has_content(education):

        return 1.0

    return 0.0


# ============================================================
# ATS PARSEABILITY
# ============================================================

def calculate_parseability_score(
    resume_profile,
    resume_text
):
    """
    Estimate whether the resume contains
    structured, machine-readable information.

    This is a heuristic and not a guarantee
    of compatibility with every ATS.
    """

    score = 0.0

    checks = {
        "name": bool(
            resume_profile.get("name")
        ),

        "email": bool(
            resume_profile.get("email")
        ),

        "phone": bool(
            resume_profile.get("phone")
        ),

        "skills": bool(
            resume_profile.get("skills")
        ),

        "education": _has_content(
            resume_profile.get(
                "education",
                ""
            )
        ),

        "experience": _has_content(
            resume_profile.get(
                "experience",
                ""
            )
        ),

        "projects": _has_content(
            resume_profile.get(
                "projects",
                ""
            )
        ),

        "readable_text": bool(
            resume_text
            and len(resume_text.strip()) > 100
        )
    }

    for value in checks.values():

        if value:

            score += 1

    score = score / len(checks)

    return {
        "score": _safe_score(score),
        "checks": checks
    }


# ============================================================
# ATS ISSUES
# ============================================================

def identify_ats_issues(
    resume_profile,
    keyword_result,
    section_result,
    parseability_result
):
    """
    Generate ATS-related issues.
    """

    issues = []

    missing_skills = keyword_result[
        "missing_skills"
    ]

    if missing_skills:

        issues.append(
            "Some job-relevant keywords are missing "
            "from the resume."
        )

    missing_sections = section_result[
        "missing_sections"
    ]

    if missing_sections:

        readable_sections = [
            section.replace(
                "_",
                " "
            ).title()
            for section in missing_sections
        ]

        issues.append(
            "The following important resume sections "
            "were not detected: "
            + ", ".join(
                readable_sections
            )
            + "."
        )

    checks = parseability_result[
        "checks"
    ]

    if not checks["name"]:

        issues.append(
            "Candidate name could not be detected."
        )

    if not checks["email"]:

        issues.append(
            "Email address could not be detected."
        )

    if not checks["phone"]:

        issues.append(
            "Phone number could not be detected."
        )

    if not checks["readable_text"]:

        issues.append(
            "The extracted resume text is too short "
            "for reliable ATS analysis."
        )

    return issues


# ============================================================
# ATS RECOMMENDATIONS
# ============================================================

def generate_ats_recommendations(
    keyword_result,
    section_result,
    experience_result,
    project_result,
    parseability_result
):
    """
    Generate actionable ATS recommendations.
    """

    recommendations = []

    missing_skills = keyword_result[
        "missing_skills"
    ]

    if missing_skills:

        recommendations.append(
            "Add missing job-relevant keywords only "
            "if you genuinely have experience or "
            "knowledge of those skills: "
            + ", ".join(
                skill.title()
                for skill in missing_skills
            )
            + "."
        )

    if section_result[
        "missing_sections"
    ]:

        recommendations.append(
            "Consider adding the missing resume "
            "sections: "
            + ", ".join(
                section.replace(
                    "_",
                    " "
                ).title()
                for section in section_result[
                    "missing_sections"
                ]
            )
            + "."
        )

    if experience_result[
        "score"
    ] < 0.50:

        recommendations.append(
            "Tailor your experience descriptions "
            "to the responsibilities and technologies "
            "mentioned in the job description."
        )

    if project_result[
        "score"
    ] < 0.50:

        recommendations.append(
            "Make project descriptions more relevant "
            "to the target role by highlighting "
            "technologies, responsibilities and outcomes."
        )

    if parseability_result[
        "score"
    ] < 0.75:

        recommendations.append(
            "Improve resume structure by clearly "
            "presenting contact information, skills, "
            "education, experience and projects."
        )

    if not recommendations:

        recommendations.append(
            "Your resume has good ATS-oriented "
            "structure and job alignment."
        )

    return recommendations


# ============================================================
# SCORE BREAKDOWN
# ============================================================

def calculate_ats_score(
    resume_profile,
    job_profile,
    semantic_score,
    embedding_model,
    resume_text
):
    """
    Calculate the final ATS Compatibility Score.

    Weighting:

    Keyword Match       = 30%
    Semantic Relevance  = 25%
    Section Completeness= 15%
    Experience          = 10%
    Education           = 5%
    Projects            = 5%
    Parseability        = 10%

    Total = 100%
    """

    # --------------------------------------------------------
    # Keyword
    # --------------------------------------------------------

    keyword_result = calculate_keyword_score(
        resume_profile.get(
            "skills",
            []
        ),
        job_profile.get(
            "skills",
            []
        )
    )

    keyword_score = keyword_result[
        "score"
    ]

    # --------------------------------------------------------
    # Semantic
    # --------------------------------------------------------

    semantic_score = _safe_score(
        semantic_score
    )

    # --------------------------------------------------------
    # Sections
    # --------------------------------------------------------

    section_result = (
        calculate_section_completeness(
            resume_profile
        )
    )

    section_score = section_result[
        "score"
    ]

    # --------------------------------------------------------
    # Experience
    # --------------------------------------------------------

    experience_result = (
        calculate_experience_relevance(
            resume_profile,
            job_profile.get(
                "description",
                ""
            ),
            embedding_model
        )
    )

    experience_score = experience_result[
        "score"
    ]

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    education_score = (
        calculate_education_score(
            resume_profile
        )
    )

    # --------------------------------------------------------
    # Projects
    # --------------------------------------------------------

    project_result = (
        calculate_project_relevance(
            resume_profile,
            job_profile.get(
                "description",
                ""
            ),
            embedding_model
        )
    )

    project_score = project_result[
        "score"
    ]

    # --------------------------------------------------------
    # Parseability
    # --------------------------------------------------------

    parseability_result = (
        calculate_parseability_score(
            resume_profile,
            resume_text
        )
    )

    parseability_score = (
        parseability_result[
            "score"
        ]
    )

    # --------------------------------------------------------
    # Weighted score
    # --------------------------------------------------------

    final_score = (

        keyword_score * 0.30

        +

        semantic_score * 0.25

        +

        section_score * 0.15

        +

        experience_score * 0.10

        +

        education_score * 0.05

        +

        project_score * 0.05

        +

        parseability_score * 0.10
    )

    final_score = max(
        0.0,
        min(
            1.0,
            float(final_score)
        )
    )

    # --------------------------------------------------------
    # Issues
    # --------------------------------------------------------

    ats_issues = identify_ats_issues(
        resume_profile,
        keyword_result,
        section_result,
        parseability_result
    )

    # --------------------------------------------------------
    # Recommendations
    # --------------------------------------------------------

    ats_recommendations = (
        generate_ats_recommendations(
            keyword_result,
            section_result,
            experience_result,
            project_result,
            parseability_result
        )
    )

    # --------------------------------------------------------
    # Score breakdown
    # --------------------------------------------------------

    score_breakdown = {

        "keyword_match": {
            "score": keyword_score,
            "weight": 0.30,
            "points": keyword_score * 30
        },

        "semantic_relevance": {
            "score": semantic_score,
            "weight": 0.25,
            "points": semantic_score * 25
        },

        "section_completeness": {
            "score": section_score,
            "weight": 0.15,
            "points": section_score * 15
        },

        "experience_relevance": {
            "score": experience_score,
            "weight": 0.10,
            "points": experience_score * 10
        },

        "education": {
            "score": education_score,
            "weight": 0.05,
            "points": education_score * 5
        },

        "project_relevance": {
            "score": project_score,
            "weight": 0.05,
            "points": project_score * 5
        },

        "parseability": {
            "score": parseability_score,
            "weight": 0.10,
            "points": parseability_score * 10
        }
    }

    return {

        "ats_score": final_score,

        "ats_score_percentage":
            final_score * 100,

        "score_breakdown":
            score_breakdown,

        "keyword_result":
            keyword_result,

        "section_result":
            section_result,

        "experience_result":
            experience_result,

        "education_score":
            education_score,

        "project_result":
            project_result,

        "parseability_result":
            parseability_result,

        "ats_issues":
            ats_issues,

        "ats_recommendations":
            ats_recommendations
    }