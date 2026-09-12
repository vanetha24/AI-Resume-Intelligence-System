import re
import pandas as pd


def load_skills(csv_path="data/skills.csv"):
    skills_df = pd.read_csv(csv_path)

    required_columns = {
        "skill",
        "category",
        "canonical"
    }

    missing_columns = (
        required_columns
        - set(skills_df.columns)
    )

    if missing_columns:
        raise ValueError(
            "skills.csv is missing columns: "
            + ", ".join(missing_columns)
        )

    return skills_df


def normalize_text(text):
    if text is None:
        return ""

    text = str(text).lower()

    text = text.replace("–", "-")
    text = text.replace("—", "-")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def build_skill_alias_map(skills_df):
    alias_map = {}

    for _, row in skills_df.iterrows():

        skill = str(
            row["skill"]
        ).lower().strip()

        canonical = str(
            row["canonical"]
        ).lower().strip()

        if skill:
            alias_map[skill] = canonical

    return alias_map


def skill_exists_in_text(text, skill):

    text = normalize_text(text)
    skill = normalize_text(skill)

    if not text or not skill:
        return False

    # Escape special regex characters
    escaped_skill = re.escape(skill)

    # Allow normal word boundaries.
    # This also works for skills such as:
    # c++, c#, .net, machine learning, etc.
    pattern = (
        r"(?<![a-zA-Z0-9])"
        + escaped_skill
        + r"(?![a-zA-Z0-9])"
    )

    return bool(
        re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )
    )


def extract_skills(text, skills_df):

    normalized_text = normalize_text(text)

    if not normalized_text:
        return []

    alias_map = build_skill_alias_map(
        skills_df
    )

    found_skills = set()

    for alias, canonical in alias_map.items():

        if skill_exists_in_text(
            normalized_text,
            alias
        ):
            found_skills.add(
                canonical
            )

    return sorted(
        found_skills
    )


def get_skill_categories(
    skills,
    skills_df
):

    result = {}

    for skill in skills:

        rows = skills_df[
            skills_df["canonical"]
            .str.lower()
            == skill.lower()
        ]

        if not rows.empty:

            category = rows.iloc[0][
                "category"
            ]

            result[skill] = category

    return result


def group_skills_by_category(
    skills,
    skills_df
):

    categories = {}

    skill_categories = get_skill_categories(
        skills,
        skills_df
    )

    for skill, category in (
        skill_categories.items()
    ):

        if category not in categories:
            categories[category] = []

        categories[category].append(
            skill
        )

    return categories