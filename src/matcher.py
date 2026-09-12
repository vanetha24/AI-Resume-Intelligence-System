from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# SEMANTIC SIMILARITY
# ============================================================

def calculate_semantic_similarity(
    resume_embedding,
    job_embedding
):
    """
    Calculate cosine similarity between
    resume and job embeddings.
    """

    score = cosine_similarity(
        [resume_embedding],
        [job_embedding]
    )[0][0]

    score = max(
        0.0,
        min(
            1.0,
            float(score)
        )
    )

    return score


# ============================================================
# SKILL MATCH
# ============================================================

def calculate_skill_match(
    resume_skills,
    job_skills
):
    """
    Compare canonical resume skills
    with canonical job skills.
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

    matched = sorted(
        resume_set.intersection(
            job_set
        )
    )

    missing = sorted(
        job_set.difference(
            resume_set
        )
    )

    additional = sorted(
        resume_set.difference(
            job_set
        )
    )

    if not job_set:

        skill_score = 0.0

    else:

        skill_score = (
            len(matched)
            /
            len(job_set)
        )

    return {

        "matched_skills":
            matched,

        "missing_skills":
            missing,

        "additional_skills":
            additional,

        "skill_score":
            skill_score
    }


# ============================================================
# CATEGORY MATCH
# ============================================================

def calculate_category_match(
    resume_skills,
    job_skills,
    skills_df
):
    """
    Compare skill categories.
    """

    resume_categories = set()

    job_categories = set()


    # Resume categories
    for skill in resume_skills:

        rows = skills_df[
            skills_df["canonical"]
            .str.lower()
            ==
            skill.lower()
        ]

        if not rows.empty:

            category = str(
                rows.iloc[0]["category"]
            ).lower()

            resume_categories.add(
                category
            )


    # Job categories
    for skill in job_skills:

        rows = skills_df[
            skills_df["canonical"]
            .str.lower()
            ==
            skill.lower()
        ]

        if not rows.empty:

            category = str(
                rows.iloc[0]["category"]
            ).lower()

            job_categories.add(
                category
            )


    matched_categories = sorted(
        resume_categories.intersection(
            job_categories
        )
    )

    missing_categories = sorted(
        job_categories.difference(
            resume_categories
        )
    )


    if not job_categories:

        category_score = 0.0

    else:

        category_score = (
            len(matched_categories)
            /
            len(job_categories)
        )


    return {

        "resume_categories":
            sorted(
                resume_categories
            ),

        "job_categories":
            sorted(
                job_categories
            ),

        "matched_categories":
            matched_categories,

        "missing_categories":
            missing_categories,

        "category_score":
            category_score
    }


# ============================================================
# CRITICAL GAPS
# ============================================================

def identify_critical_gaps(
    missing_skills,
    skills_df
):
    """
    Identify missing skills that belong
    to high-priority technical categories.
    """

    critical_gaps = []


    priority_categories = {

        "programming",

        "ai",

        "database",

        "backend",

        "cloud"
    }


    for skill in missing_skills:

        rows = skills_df[
            skills_df["canonical"]
            .str.lower()
            ==
            skill.lower()
        ]

        if rows.empty:

            continue


        category = str(
            rows.iloc[0]["category"]
        ).lower()


        if category in priority_categories:

            critical_gaps.append({

                "skill":
                    skill,

                "category":
                    category
            })


    return critical_gaps


# ============================================================
# OVERALL SCORE
# ============================================================

def calculate_overall_score(
    semantic_score,
    skill_score
):
    """
    Calculate final compatibility score.

    65% semantic similarity
    35% explicit skill match
    """

    overall_score = (

        semantic_score
        * 0.65

        +

        skill_score
        * 0.35
    )

    return max(

        0.0,

        min(

            1.0,

            float(
                overall_score
            )
        )
    )