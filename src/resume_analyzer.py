import re


# =========================================================
# SECTION DEFINITIONS
# =========================================================

SECTION_ALIASES = {

    "summary": [
        "summary",
        "professional summary",
        "profile",
        "profile summary",
        "professional profile",
        "career objective",
        "objective",
        "about me"
    ],

    "education": [
        "education",
        "educational background",
        "educational qualification",
        "educational qualifications",
        "academic background",
        "academic qualification",
        "academic qualifications",
        "academic profile",
        "academic details",
        "qualifications",
        "qualification"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
        "career history",
        "professional background",
        "internship experience",
        "internship",
        "internships",
        "work experience and internships",
        "experience and internships"
    ],

    "projects": [
        "projects",
        "project",
        "academic projects",
        "personal projects",
        "major projects",
        "project experience",
        "project work",
        "academic project",
        "projects and research",
        "research projects"
    ],

    "skills": [
        "skills",
        "technical skills",
        "technical skill",
        "core skills",
        "key skills",
        "professional skills",
        "skills summary",
        "technical competencies",
        "technical competency",
        "competencies",
        "core competencies"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "professional certifications",
        "courses",
        "courses and certifications"
    ],

    "achievements": [
        "achievements",
        "accomplishments",
        "awards",
        "honors"
    ],

    "publications": [
        "publications",
        "research publications",
        "research papers",
        "papers",
        "academic publications",
        "research work",
        "research"
    ]
}


# =========================================================
# BASIC INFORMATION
# =========================================================

def extract_email(text):
    """
    Extract email address from resume.
    """

    pattern = (
        r"[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+"
        r"\.[A-Za-z]{2,}"
    )

    match = re.search(pattern, text)

    if match:
        return match.group(0)

    return None


def extract_phone(text):
    """
    Extract phone number from resume.
    """

    patterns = [

        r"(?:\+91[\s-]?)?[6-9]\d{9}",

        r"\+91[\s-]?\d{5}[\s-]?\d{5}",

        r"\d{3}[\s-]\d{3}[\s-]\d{4}"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:
            return match.group(0)

    return None


def extract_name(text):
    """
    Detect the candidate name from the resume.

    The function uses several signals:
    1. Looks near the beginning of the resume.
    2. Ignores email, phone, URLs and common resume labels.
    3. Prefers short name-like lines.
    4. Handles names containing initials.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    ignored_exact = {
        "resume",
        "cv",
        "curriculum vitae",
        "profile",
        "summary",
        "professional summary",
        "career objective",
        "objective",
        "contact",
        "contact information",
        "email",
        "phone",
        "mobile",
        "linkedin",
        "github",
        "portfolio",
        "education",
        "skills",
        "technical skills",
        "experience",
        "work experience",
        "professional experience",
        "projects",
        "certifications",
        "achievements",
        "publications"
    }

    ignored_words = {
        "resume",
        "curriculum",
        "vitae",
        "profile",
        "summary",
        "objective",
        "contact",
        "email",
        "phone",
        "mobile",
        "linkedin",
        "github",
        "portfolio",
        "education",
        "skills",
        "experience",
        "projects",
        "certifications",
        "achievements",
        "publications",
        "developer",
        "engineer",
        "student",
        "intern",
        "enthusiast"
    }

    candidates = []

    # Check more lines because PDF extraction
    # may not preserve visual positioning.
    for index, line in enumerate(lines[:40]):

        cleaned = line.strip()

        lower = cleaned.lower()

        # Ignore known headings.
        if lower in ignored_exact:
            continue

        # Ignore email addresses.
        if "@" in cleaned:
            continue

        # Ignore URLs.
        if (
            "http://" in lower
            or "https://" in lower
            or "www." in lower
        ):
            continue

        # Ignore lines containing phone numbers.
        if re.search(
            r"\+?\d[\d\s().-]{7,}",
            cleaned
        ):
            continue

        # Remove common separators.
        name_candidate = re.sub(
            r"[|•●▪■:]+",
            " ",
            cleaned
        )

        name_candidate = re.sub(
            r"\s+",
            " ",
            name_candidate
        ).strip()

        words = name_candidate.split()

        # Names are usually short.
        if not (2 <= len(words) <= 5):
            continue

        # Reject very long sentences.
        if len(name_candidate) > 60:
            continue

        # Check every word.
        valid_name = True

        for word in words:

            word_lower = word.lower()

            # Remove punctuation around the word.
            clean_word = re.sub(
                r"[^a-zA-Z.'-]",
                "",
                word
            )

            if not clean_word:
                valid_name = False
                break

            # Reject obvious resume words.
            if clean_word.lower() in ignored_words:
                valid_name = False
                break

            # Names should contain alphabetic characters.
            if not re.search(
                r"[A-Za-z]",
                clean_word
            ):
                valid_name = False
                break

        if not valid_name:
            continue

        # Count uppercase letters.
        uppercase_count = sum(
            1
            for char in name_candidate
            if char.isupper()
        )

        # Count alphabetic characters.
        alphabetic_count = sum(
            1
            for char in name_candidate
            if char.isalpha()
        )

        uppercase_ratio = (
            uppercase_count / alphabetic_count
            if alphabetic_count
            else 0
        )

        # Name-like score.
        score = 0

        # Names appearing near the beginning
        # receive a higher score.
        score += max(
            0,
            20 - index
        )

        # 2-4 word names are common.
        if 2 <= len(words) <= 4:
            score += 20

        # Names with title-case or uppercase formatting
        # are more likely to be actual names.
        if uppercase_ratio >= 0.5:
            score += 15

        # Avoid lines that look like job titles.
        job_title_words = {
            "developer",
            "engineer",
            "analyst",
            "manager",
            "designer",
            "student",
            "intern",
            "consultant",
            "specialist",
            "architect",
            "scientist"
        }

        if any(
            word.lower() in job_title_words
            for word in words
        ):
            score -= 20

        candidates.append(
            (
                score,
                index,
                name_candidate
            )
        )

    if not candidates:
        return None

    # Highest scoring candidate.
    candidates.sort(
        key=lambda item: (
            item[0],
            -item[1]
        ),
        reverse=True
    )

    return candidates[0][2]


# =========================================================
# HEADING NORMALIZATION
# =========================================================

def normalize_heading(text):
    """
    Normalize a possible resume heading.
    """

    text = text.strip().lower()

    # Remove bullet characters
    text = re.sub(
        r"^[•●▪■◦\-]+\s*",
        "",
        text
    )

    # Replace ampersand
    text = text.replace(
        "&",
        "and"
    )

    # Remove punctuation at end
    text = re.sub(
        r"[:\-|]+$",
        "",
        text
    )

    # Normalize spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def is_section_heading(line):
    """
    Check whether a line is a known
    resume section heading.
    """

    normalized = normalize_heading(
        line
    )

    for section_name, aliases in SECTION_ALIASES.items():

        for alias in aliases:

            if normalized == alias:

                return section_name

    return None


# =========================================================
# SECTION EXTRACTION
# =========================================================

def extract_section(
    text,
    target_section
):
    """
    Extract content belonging to a
    particular resume section.
    """

    lines = text.splitlines()

    collecting = False

    section_lines = []

    for line in lines:

        stripped = line.strip()

        if not stripped:

            if collecting:
                section_lines.append("")

            continue

        detected_section = is_section_heading(
            stripped
        )

        # ---------------------------------------------
        # Start target section
        # ---------------------------------------------

        if detected_section == target_section:

            collecting = True

            continue

        # ---------------------------------------------
        # Stop when another known section begins
        # ---------------------------------------------

        if (
            collecting
            and detected_section is not None
        ):

            break

        # ---------------------------------------------
        # Collect section content
        # ---------------------------------------------

        if collecting:

            section_lines.append(
                stripped
            )

    result = "\n".join(
        section_lines
    )

    # Remove excessive blank lines
    result = re.sub(
        r"\n{2,}",
        "\n",
        result
    )

    return result.strip()


# =========================================================
# SECTION FUNCTIONS
# =========================================================

def extract_summary(text):

    return extract_section(
        text,
        "summary"
    )


def extract_education(text):

    return extract_section(
        text,
        "education"
    )


def extract_experience(text):

    return extract_section(
        text,
        "experience"
    )


def extract_projects(text):

    return extract_section(
        text,
        "projects"
    )


def extract_skills_section(text):

    return extract_section(
        text,
        "skills"
    )


def extract_certifications(text):

    return extract_section(
        text,
        "certifications"
    )


def extract_achievements(text):

    return extract_section(
        text,
        "achievements"
    )


def extract_publications(text):

    return extract_section(
        text,
        "publications"
    )


# =========================================================
# COMPLETE RESUME ANALYSIS
# =========================================================

def analyze_resume(
    text,
    skills_df
):
    """
    Create a structured candidate profile
    from the resume.
    """

    from src.skill_extractor import (
        extract_skills
    )

    skills = extract_skills(
        text,
        skills_df
    )

    profile = {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "summary": extract_summary(text),

        "skills": skills,

        "education": extract_education(
            text
        ),

        "experience": extract_experience(
            text
        ),

        "projects": extract_projects(
            text
        ),

        "certifications": extract_certifications(
            text
        ),

        "achievements": extract_achievements(
            text
        ),

        "publications": extract_publications(
            text
        )
    }

    return profile