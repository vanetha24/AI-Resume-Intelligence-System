import re


def clean_text(text: str) -> str:
    """
    Clean extracted resume text.
    """

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces
    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    # Remove excessive blank lines
    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def normalize_for_matching(text: str) -> str:
    """
    Normalize text for skill matching.
    """

    text = text.lower()

    text = text.replace(
        "&",
        " and "
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()