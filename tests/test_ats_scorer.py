from src.ats_scorer import (
    calculate_keyword_score,
    calculate_section_completeness,
    calculate_education_score,
    calculate_parseability_score
)


def test_keyword_score():

    result = calculate_keyword_score(
        [
            "python",
            "machine learning",
            "pandas"
        ],
        [
            "python",
            "machine learning",
            "sql"
        ]
    )

    assert result["score"] == 2 / 3

    assert "python" in (
        result["matched_skills"]
    )

    assert "sql" in (
        result["missing_skills"]
    )


def test_section_completeness():

    profile = {

        "summary":
            "AI enthusiast",

        "skills": [
            "python"
        ],

        "education":
            "MCA",

        "experience":
            "",

        "projects":
            "AI Resume Project"
    }

    result = calculate_section_completeness(
        profile
    )

    assert result["score"] == 0.8

    assert "experience" in (
        result["missing_sections"]
    )


def test_education_score_present():

    profile = {
        "education": "MCA"
    }

    score = calculate_education_score(
        profile
    )

    assert score == 1.0


def test_education_score_missing():

    profile = {
        "education": ""
    }

    score = calculate_education_score(
        profile
    )

    assert score == 0.0


def test_parseability_score():

    profile = {

        "name": "John Doe",

        "email":
            "john@example.com",

        "phone":
            "+91 9876543210",

        "skills": [
            "python"
        ],

        "education":
            "MCA",

        "experience":
            "ML Intern",

        "projects":
            "AI Project"
    }

    result = calculate_parseability_score(
        profile,
        "This is a readable resume "
        "with enough extracted text."
    )

    assert result["score"] > 0.5