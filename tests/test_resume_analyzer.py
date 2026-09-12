
from src.resume_analyzer import (
    extract_email,
    extract_phone,
    extract_name,
    extract_section,
    analyze_resume
)

from src.skill_extractor import load_skills


def test_extract_email():

    text = """
    John Doe
    john.doe@gmail.com
    """

    email = extract_email(text)

    assert email == "john.doe@gmail.com"


def test_extract_phone():

    text = """
    John Doe
    +91 9876543210
    """

    phone = extract_phone(text)

    assert phone is not None

    assert "9876543210" in (
        phone
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )


def test_extract_name():

    text = """
    JOHN DOE
    john.doe@gmail.com
    +91 9876543210

    PROFESSIONAL SUMMARY

    AI and ML enthusiast with Python experience.
    """

    name = extract_name(text)

    assert name == "JOHN DOE"


def test_extract_section():

    text = """
    PROFESSIONAL SUMMARY

    AI and ML enthusiast with Python experience.

    EDUCATION

    Master of Computer Applications
    Anna University

    PROJECTS

    AI Resume Intelligence System
    """

    summary = extract_section(
        text,
        "summary"
    )

    education = extract_section(
        text,
        "education"
    )

    projects = extract_section(
        text,
        "projects"
    )

    assert (
        "AI and ML enthusiast"
        in summary
    )

    assert (
        "Master of Computer Applications"
        in education
    )

    assert (
        "AI Resume Intelligence System"
        in projects
    )


def test_analyze_resume():

    text = """
    JOHN DOE
    john.doe@gmail.com
    +91 9876543210

    PROFESSIONAL SUMMARY

    AI and ML enthusiast with Python experience.

    EDUCATION

    Master of Computer Applications
    Anna University

    PROJECTS

    AI Resume Intelligence System

    SKILLS

    Python, Machine Learning, NLP
    """

    skills_df = load_skills()

    profile = analyze_resume(
        text,
        skills_df
    )

    assert profile["name"] == "JOHN DOE"

    assert (
        profile["email"]
        == "john.doe@gmail.com"
    )

    assert profile["skills"]

    assert "summary" in profile

    assert "education" in profile

    assert "projects" in profile

