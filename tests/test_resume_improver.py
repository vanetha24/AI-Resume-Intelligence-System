from src.resume_improver import (
    calculate_skill_keyword_coverage,
    calculate_resume_improvement_score,
    identify_resume_strengths,
    identify_resume_weaknesses,
    generate_improvement_recommendations,
    analyze_resume_improvement
)


def test_skill_keyword_coverage():

    resume_skills = [
        "python",
        "machine learning",
        "pandas"
    ]

    job_skills = [
        "python",
        "machine learning",
        "sql",
        "docker"
    ]

    result = calculate_skill_keyword_coverage(
        resume_skills,
        job_skills
    )

    assert result["total_job_skills"] == 4

    assert result["matched_skills"] == [
        "machine learning",
        "python"
    ]

    assert result["missing_skills"] == [
        "docker",
        "sql"
    ]

    assert result["coverage"] == 0.5


def test_skill_keyword_coverage_full_match():

    resume_skills = [
        "python",
        "machine learning",
        "sql"
    ]

    job_skills = [
        "python",
        "machine learning",
        "sql"
    ]

    result = calculate_skill_keyword_coverage(
        resume_skills,
        job_skills
    )

    assert result["total_job_skills"] == 3

    assert result["matched_skills"] == [
        "machine learning",
        "python",
        "sql"
    ]

    assert result["missing_skills"] == []

    assert result["coverage"] == 1.0


def test_skill_keyword_coverage_no_job_skills():

    resume_skills = [
        "python",
        "machine learning"
    ]

    job_skills = []

    result = calculate_skill_keyword_coverage(
        resume_skills,
        job_skills
    )

    assert result["total_job_skills"] == 0

    assert result["matched_skills"] == []

    assert result["missing_skills"] == []

    assert result["coverage"] == 0.0


def test_resume_improvement_score():

    profile = {
        "summary": (
            "AI and ML enthusiast with experience "
            "building machine learning projects "
            "using Python and NLP."
        ),
        "projects": (
            "AI Resume Intelligence System"
        ),
        "education": (
            "Master of Computer Applications"
        ),
        "experience": (
            "Machine Learning Intern"
        ),
        "certifications": (
            "Machine Learning Certification"
        )
    }

    skill_coverage = {
        "coverage": 0.80
    }

    score = calculate_resume_improvement_score(
        profile,
        skill_coverage
    )

    assert 0.0 <= score <= 100.0

    assert score == 88.0


def test_resume_improvement_score_empty_profile():

    profile = {
        "summary": "",
        "projects": "",
        "education": "",
        "experience": "",
        "certifications": "",
        "achievements": "",
        "publications": ""
    }

    skill_coverage = {
        "coverage": 0.0
    }

    score = calculate_resume_improvement_score(
        profile,
        skill_coverage
    )

    assert score == 0.0


def test_identify_resume_strengths():

    profile = {
        "summary": (
            "AI and ML enthusiast with experience "
            "in Python, NLP and machine learning "
            "projects."
        ),
        "projects": (
            "AI Resume Intelligence System"
        ),
        "education": (
            "Master of Computer Applications"
        ),
        "experience": (
            "Machine Learning Intern"
        ),
        "certifications": (
            "Machine Learning Certification"
        )
    }

    skill_coverage = {
        "coverage": 0.90
    }

    strengths = identify_resume_strengths(
        profile,
        skill_coverage
    )

    assert isinstance(
        strengths,
        list
    )

    assert len(strengths) > 0

    assert any(
        "Strong coverage"
        in strength
        for strength in strengths
    )

    assert any(
        "Projects are present"
        in strength
        for strength in strengths
    )


def test_identify_resume_weaknesses():

    profile = {
        "summary": "",
        "projects": "",
        "education": "",
        "experience": "",
        "skills": []
    }

    skill_coverage = {
        "coverage": 0.25,
        "missing_skills": [
            "python",
            "machine learning"
        ]
    }

    weaknesses = identify_resume_weaknesses(
        profile,
        skill_coverage
    )

    assert isinstance(
        weaknesses,
        list
    )

    assert len(weaknesses) > 0

    assert any(
        "skills required"
        in weakness
        for weakness in weaknesses
    )

    assert any(
        "professional summary"
        in weakness
        for weakness in weaknesses
    )

    assert any(
        "project section"
        in weakness
        for weakness in weaknesses
    )

    assert any(
        "experience section"
        in weakness
        for weakness in weaknesses
    )

    assert any(
        "technical skills"
        in weakness
        for weakness in weaknesses
    )


def test_generate_improvement_recommendations():

    profile = {
        "summary": "",
        "projects": "",
        "education": "",
        "experience": "",
        "skills": []
    }

    skill_coverage = {
        "coverage": 0.25,
        "missing_skills": [
            "python",
            "machine learning"
        ]
    }

    recommendations = (
        generate_improvement_recommendations(
            profile,
            skill_coverage
        )
    )

    assert isinstance(
        recommendations,
        list
    )

    assert len(recommendations) > 0

    combined_text = " ".join(
        recommendations
    ).lower()

    assert "python" in combined_text

    assert (
        "machine learning"
        in combined_text
    )

    assert "50%" in combined_text

    assert "summary" in combined_text

    assert "projects" in combined_text


def test_analyze_resume_improvement():

    profile = {
        "summary": (
            "AI and ML enthusiast with experience "
            "building machine learning projects."
        ),
        "projects": (
            "AI Resume Intelligence System"
        ),
        "education": (
            "Master of Computer Applications"
        ),
        "experience": "",
        "skills": [
            "python",
            "machine learning"
        ]
    }

    job_profile = {
        "skills": [
            "python",
            "machine learning",
            "sql",
            "docker"
        ]
    }

    result = analyze_resume_improvement(
        profile,
        job_profile
    )

    assert isinstance(
        result,
        dict
    )

    assert (
        "improvement_score"
        in result
    )

    assert (
        "skill_coverage"
        in result
    )

    assert "strengths" in result

    assert "weaknesses" in result

    assert "recommendations" in result

    assert (
        result["skill_coverage"]["coverage"]
        == 0.5
    )

    assert (
        result["skill_coverage"]["missing_skills"]
        == [
            "docker",
            "sql"
        ]
    )

    assert (
        0.0
        <= result["improvement_score"]
        <= 100.0
    )

    assert len(
        result["strengths"]
    ) > 0

    assert len(
        result["weaknesses"]
    ) > 0

    assert len(
        result["recommendations"]
    ) > 0
