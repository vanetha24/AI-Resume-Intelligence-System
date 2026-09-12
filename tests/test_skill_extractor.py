from src.skill_extractor import (
    load_skills,
    extract_skills
)


def test_python_skill():

    skills_df = load_skills()

    skills = extract_skills(
        "I have experience with Python.",
        skills_df
    )

    assert "python" in skills


def test_machine_learning_alias():

    skills_df = load_skills()

    skills = extract_skills(
        "I have experience with ML.",
        skills_df
    )

    assert "machine learning" in skills


def test_nlp_alias():

    skills_df = load_skills()

    skills = extract_skills(
        "I have experience with Natural Language Processing.",
        skills_df
    )

    assert "nlp" in skills


def test_llm_alias():

    skills_df = load_skills()

    skills = extract_skills(
        "I worked with Large Language Models.",
        skills_df
    )

    assert "llm" in skills


def test_empty_text():

    skills_df = load_skills()

    skills = extract_skills(
        "",
        skills_df
    )

    assert skills == []