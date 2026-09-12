from src.matcher import (
    calculate_semantic_similarity,
    calculate_skill_match,
    calculate_category_match,
    identify_critical_gaps,
    calculate_overall_score
)

from src.skill_extractor import load_skills


def test_semantic_similarity_identical_vectors():

    resume_embedding = [1.0, 0.0, 0.0]

    job_embedding = [1.0, 0.0, 0.0]

    score = calculate_semantic_similarity(
        resume_embedding,
        job_embedding
    )

    assert score == 1.0


def test_semantic_similarity_different_vectors():

    resume_embedding = [1.0, 0.0, 0.0]

    job_embedding = [0.0, 1.0, 0.0]

    score = calculate_semantic_similarity(
        resume_embedding,
        job_embedding
    )

    assert score == 0.0


def test_skill_match():

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

    result = calculate_skill_match(
        resume_skills,
        job_skills
    )

    assert result["matched_skills"] == [
        "machine learning",
        "python"
    ]

    assert result["missing_skills"] == [
        "docker",
        "sql"
    ]

    assert result["additional_skills"] == [
        "pandas"
    ]

    assert result["skill_score"] == 0.5


def test_skill_match_with_no_job_skills():

    resume_skills = [
        "python",
        "machine learning"
    ]

    job_skills = []

    result = calculate_skill_match(
        resume_skills,
        job_skills
    )

    assert result["matched_skills"] == []

    assert result["missing_skills"] == []

    assert result["additional_skills"] == [
        "machine learning",
        "python"
    ]

    assert result["skill_score"] == 0.0


def test_category_match():

    skills_df = load_skills()

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

    result = calculate_category_match(
        resume_skills,
        job_skills,
        skills_df
    )

    assert "programming" in (
        result["matched_categories"]
    )

    assert "ai" in (
        result["matched_categories"]
    )

    assert "database" in (
        result["missing_categories"]
    )

    assert "devops" in (
        result["missing_categories"]
    )


def test_critical_gaps():

    skills_df = load_skills()

    missing_skills = [
        "python",
        "machine learning",
        "sql",
        "docker",
        "html"
    ]

    critical_gaps = identify_critical_gaps(
        missing_skills,
        skills_df
    )

    critical_skill_names = [
        item["skill"]
        for item in critical_gaps
    ]

    assert "python" in critical_skill_names

    assert (
        "machine learning"
        in critical_skill_names
    )

    assert "sql" in critical_skill_names

    assert "docker" not in critical_skill_names

    assert "html" not in critical_skill_names


def test_overall_score():

    semantic_score = 0.80

    skill_score = 0.60

    score = calculate_overall_score(
        semantic_score,
        skill_score
    )

    expected_score = (
        0.80 * 0.65
        +
        0.60 * 0.35
    )

    assert score == expected_score


def test_overall_score_is_between_zero_and_one():

    score = calculate_overall_score(
        1.5,
        -0.5
    )

    assert 0.0 <= score <= 1.0

