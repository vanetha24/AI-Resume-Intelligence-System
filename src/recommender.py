def generate_recommendations(
    missing_skills,
    semantic_score,
    skill_score
):
    """
    Generate personalized recommendations
    based on matching results.
    """

    recommendations = []

    # ---------------------------------------
    # SKILL GAP
    # ---------------------------------------

    if missing_skills:

        skill_text = ", ".join(
            skill.title()
            for skill in missing_skills
        )

        recommendations.append(
            "Skill Gap: Consider developing "
            "these job-relevant skills: "
            + skill_text
            + "."
        )

    else:

        recommendations.append(
            "Skill Gap: No missing skills "
            "were detected from the current "
            "skill knowledge base."
        )

    # ---------------------------------------
    # SKILL MATCH
    # ---------------------------------------

    if skill_score < 0.40:

        recommendations.append(
            "Your explicit skill alignment "
            "is low. Consider developing "
            "additional technical skills "
            "required by the target role."
        )

    elif skill_score < 0.70:

        recommendations.append(
            "Your explicit skill alignment "
            "is moderate. Strengthening "
            "the missing skills could "
            "improve your profile."
        )

    else:

        recommendations.append(
            "Your resume demonstrates "
            "strong explicit skill alignment "
            "with this role."
        )

    # ---------------------------------------
    # SEMANTIC MATCH
    # ---------------------------------------

    if semantic_score < 0.40:

        recommendations.append(
            "Semantic relevance is low. "
            "Consider tailoring your resume "
            "summary and project descriptions "
            "toward the target role."
        )

    elif semantic_score < 0.70:

        recommendations.append(
            "Semantic relevance is moderate. "
            "Use job-relevant terminology "
            "naturally in your resume."
        )

    else:

        recommendations.append(
            "Your resume content has strong "
            "semantic relevance to the target "
            "job description."
        )

    return recommendations