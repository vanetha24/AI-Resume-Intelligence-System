from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_text(value):
    """
    Convert values safely into printable text.
    """

    if value is None:
        return "Not available"

    if isinstance(value, str):

        value = value.strip()

        if not value:
            return "Not available"

        return value

    return str(value)


def format_percentage(value):
    """
    Convert decimal score into percentage.
    """

    try:

        return f"{float(value) * 100:.1f}%"

    except Exception:

        return "0.0%"


def make_bullet_list(
    items,
    styles
):
    """
    Convert a list into report paragraphs.
    """

    elements = []

    if not items:

        elements.append(
            Paragraph(
                "None detected.",
                styles["BodyText"]
            )
        )

        return elements

    for item in items:

        elements.append(
            Paragraph(
                f"• {safe_text(item)}",
                styles["BodyText"]
            )
        )

        elements.append(
            Spacer(
                1,
                3
            )
        )

    return elements


def make_skill_table(
    title,
    skills,
    styles
):
    """
    Create a simple skill table.
    """

    data = [
        [
            Paragraph(
                title,
                styles["TableHeader"]
            )
        ]
    ]

    if skills:

        for skill in skills:

            data.append(
                [
                    Paragraph(
                        safe_text(
                            skill
                        ).title(),
                        styles["BodyText"]
                    )
                ]
            )

    else:

        data.append(
            [
                Paragraph(
                    "None",
                    styles["BodyText"]
                )
            ]
        )

    table = Table(
        data,
        colWidths=[
            170 * mm
        ]
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ]
        )
    )

    return table


# ============================================================
# PDF GENERATOR
# ============================================================

def generate_resume_report(
    resume_profile,
    job_profile,
    semantic_score,
    skill_score,
    overall_score,
    skill_result,
    critical_gaps,
    improvement_result
):
    """
    Generate a complete PDF resume analysis report.

    Returns:
        BytesIO object containing the PDF.
    """

    buffer = BytesIO()


    # ========================================================
    # DOCUMENT
    # ========================================================

    document = SimpleDocTemplate(

        buffer,

        pagesize=A4,

        rightMargin=20 * mm,

        leftMargin=20 * mm,

        topMargin=18 * mm,

        bottomMargin=18 * mm
    )


    # ========================================================
    # STYLES
    # ========================================================

    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(

        "ReportTitle",

        parent=styles["Title"],

        fontSize=22,

        leading=28,

        alignment=TA_CENTER,

        spaceAfter=12
    )


    subtitle_style = ParagraphStyle(

        "Subtitle",

        parent=styles["Normal"],

        fontSize=10,

        leading=14,

        alignment=TA_CENTER,

        spaceAfter=20
    )


    heading_style = ParagraphStyle(

        "SectionHeading",

        parent=styles["Heading2"],

        fontSize=15,

        leading=19,

        spaceBefore=12,

        spaceAfter=8
    )


    subheading_style = ParagraphStyle(

        "SubHeading",

        parent=styles["Heading3"],

        fontSize=12,

        leading=15,

        spaceBefore=8,

        spaceAfter=5
    )


    body_style = ParagraphStyle(

        "BodyTextCustom",

        parent=styles["BodyText"],

        fontSize=9.5,

        leading=14,

        spaceAfter=5
    )


    table_header_style = ParagraphStyle(

        "TableHeader",

        parent=styles["BodyText"],

        fontSize=9,

        leading=12
    )


    styles.add(
        body_style
    )

    styles.add(
        table_header_style
    )


    # ========================================================
    # STORY
    # ========================================================

    story = []


    # ========================================================
    # TITLE
    # ========================================================

    story.append(

        Paragraph(

            "AI Resume Intelligence Report",

            title_style
        )
    )


    story.append(

        Paragraph(

            "AI-Powered Resume Intelligence "
            "and Job Matching System",

            subtitle_style
        )
    )


    story.append(
        Spacer(
            1,
            5
        )
    )


    # ========================================================
    # CANDIDATE INFORMATION
    # ========================================================

    story.append(

        Paragraph(

            "1. Candidate Information",

            heading_style
        )
    )


    candidate_data = [

        [
            Paragraph(
                "<b>Field</b>",
                table_header_style
            ),

            Paragraph(
                "<b>Information</b>",
                table_header_style
            )
        ],

        [
            Paragraph(
                "Name",
                body_style
            ),

            Paragraph(
                safe_text(
                    resume_profile.get(
                        "name"
                    )
                ),

                body_style
            )
        ],

        [
            Paragraph(
                "Email",
                body_style
            ),

            Paragraph(
                safe_text(
                    resume_profile.get(
                        "email"
                    )
                ),

                body_style
            )
        ],

        [
            Paragraph(
                "Phone",
                body_style
            ),

            Paragraph(
                safe_text(
                    resume_profile.get(
                        "phone"
                    )
                ),

                body_style
            )
        ]
    ]


    candidate_table = Table(

        candidate_data,

        colWidths=[
            40 * mm,
            130 * mm
        ]
    )


    candidate_table.setStyle(

        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ]
        )
    )


    story.append(
        candidate_table
    )


    # ========================================================
    # RESUME SKILLS
    # ========================================================

    story.append(

        Paragraph(

            "2. Resume Skills",

            heading_style
        )
    )


    story.append(

        make_skill_table(

            "Detected Technical Skills",

            resume_profile.get(
                "skills",
                []
            ),

            styles
        )
    )


    # ========================================================
    # EDUCATION
    # ========================================================

    story.append(

        Paragraph(

            "3. Education",

            heading_style
        )
    )


    story.append(

        Paragraph(

            safe_text(
                resume_profile.get(
                    "education"
                )
            ),

            body_style
        )
    )


    # ========================================================
    # EXPERIENCE
    # ========================================================

    story.append(

        Paragraph(

            "4. Experience",

            heading_style
        )
    )


    story.append(

        Paragraph(

            safe_text(
                resume_profile.get(
                    "experience"
                )
            ),

            body_style
        )
    )


    # ========================================================
    # PROJECTS
    # ========================================================

    story.append(

        Paragraph(

            "5. Projects",

            heading_style
        )
    )


    story.append(

        Paragraph(

            safe_text(
                resume_profile.get(
                    "projects"
                )
            ),

            body_style
        )
    )


    # ========================================================
    # TARGET JOB
    # ========================================================

    story.append(
        PageBreak()
    )


    story.append(

        Paragraph(

            "6. Target Job Analysis",

            heading_style
        )
    )


    story.append(

        Paragraph(

            "<b>Detected Job Skills</b>",

            subheading_style
        )
    )


    story.append(

        make_skill_table(

            "Required Skills",

            job_profile.get(
                "skills",
                []
            ),

            styles
        )
    )


    story.append(
        Spacer(
            1,
            8
        )
    )


    story.append(

        Paragraph(

            "<b>Job Description</b>",

            subheading_style
        )
    )


    job_description = safe_text(

        job_profile.get(
            "description"
        )
    )


    story.append(

        Paragraph(

            job_description.replace(
                "\n",
                "<br/>"
            ),

            body_style
        )
    )


    # ========================================================
    # JOB MATCHING
    # ========================================================

    story.append(

        Paragraph(

            "7. Job Compatibility",

            heading_style
        )
    )


    score_data = [

        [
            Paragraph(
                "<b>Metric</b>",
                table_header_style
            ),

            Paragraph(
                "<b>Score</b>",
                table_header_style
            )
        ],

        [
            Paragraph(
                "Semantic Similarity",
                body_style
            ),

            Paragraph(
                format_percentage(
                    semantic_score
                ),
                body_style
            )
        ],

        [
            Paragraph(
                "Explicit Skill Match",
                body_style
            ),

            Paragraph(
                format_percentage(
                    skill_score
                ),
                body_style
            )
        ],

        [
            Paragraph(
                "Overall Job Match",
                body_style
            ),

            Paragraph(
                format_percentage(
                    overall_score
                ),
                body_style
            )
        ]
    ]


    score_table = Table(

        score_data,

        colWidths=[
            100 * mm,
            70 * mm
        ]
    )


    score_table.setStyle(

        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),

                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),

                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),

                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ]
        )
    )


    story.append(
        score_table
    )


    story.append(
        Spacer(
            1,
            8
        )
    )


    story.append(

        Paragraph(

            "Scoring Method: Overall Match = "
            "65% semantic similarity + "
            "35% explicit skill overlap.",

            body_style
        )
    )


    # ========================================================
    # MATCHED SKILLS
    # ========================================================

    story.append(

        Paragraph(

            "8. Matched Skills",

            heading_style
        )
    )


    story.extend(

        make_bullet_list(

            skill_result.get(
                "matched_skills",
                []
            ),

            styles
        )
    )


    # ========================================================
    # MISSING SKILLS
    # ========================================================

    story.append(

        Paragraph(

            "9. Missing Skills",

            heading_style
        )
    )


    story.extend(

        make_bullet_list(

            skill_result.get(
                "missing_skills",
                []
            ),

            styles
        )
    )


    # ========================================================
    # ADDITIONAL SKILLS
    # ========================================================

    story.append(

        Paragraph(

            "10. Additional Resume Skills",

            heading_style
        )
    )


    story.extend(

        make_bullet_list(

            skill_result.get(
                "additional_skills",
                []
            ),

            styles
        )
    )


    # ========================================================
    # CRITICAL GAPS
    # ========================================================

    story.append(

        Paragraph(

            "11. Critical Skill Gaps",

            heading_style
        )
    )


    if critical_gaps:

        for gap in critical_gaps:

            skill = safe_text(
                gap.get(
                    "skill"
                )
            ).title()

            category = safe_text(
                gap.get(
                    "category"
                )
            ).title()

            story.append(

                Paragraph(

                    f"• {skill} "
                    f"({category})",

                    body_style
                )
            )

    else:

        story.append(

            Paragraph(

                "No major critical skill gaps "
                "were detected.",

                body_style
            )
        )


    # ========================================================
    # RESUME IMPROVEMENT
    # ========================================================

    story.append(
        PageBreak()
    )


    story.append(

        Paragraph(

            "12. Resume Improvement Intelligence",

            heading_style
        )
    )


    improvement_score = (
        improvement_result.get(
            "improvement_score",
            0
        )
    )


    story.append(

        Paragraph(

            f"<b>Resume Improvement Score:</b> "
            f"{improvement_score:.1f}/100",

            body_style
        )
    )


    story.append(

        Paragraph(

            "This is a project-specific heuristic "
            "score and is not an official ATS score.",

            body_style
        )
    )


    # ========================================================
    # SKILL COVERAGE
    # ========================================================

    skill_coverage = (
        improvement_result.get(
            "skill_coverage",
            {}
        )
    )


    story.append(

        Paragraph(

            "13. Job Skill Coverage",

            heading_style
        )
    )


    coverage_data = [

        [
            Paragraph(
                "<b>Metric</b>",
                table_header_style
            ),

            Paragraph(
                "<b>Value</b>",
                table_header_style
            )
        ],

        [
            Paragraph(
                "Required Job Skills",
                body_style
            ),

            Paragraph(
                str(
                    skill_coverage.get(
                        "total_job_skills",
                        0
                    )
                ),

                body_style
            )
        ],

        [
            Paragraph(
                "Matched Skills",
                body_style
            ),

            Paragraph(
                str(
                    len(
                        skill_coverage.get(
                            "matched_skills",
                            []
                        )
                    )
                ),

                body_style
            )
        ],

        [
            Paragraph(
                "Coverage",
                body_style
            ),

            Paragraph(
                format_percentage(
                    skill_coverage.get(
                        "coverage",
                        0
                    )
                ),

                body_style
            )
        ]
    ]


    coverage_table = Table(

        coverage_data,

        colWidths=[
            100 * mm,
            70 * mm
        ]
    )


    coverage_table.setStyle(

        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.lightgrey
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                )
            ]
        )
    )


    story.append(
        coverage_table
    )


    # ========================================================
    # STRENGTHS
    # ========================================================

    story.append(

        Paragraph(

            "14. Resume Strengths",

            heading_style
        )
    )


    story.extend(

        make_bullet_list(

            improvement_result.get(
                "strengths",
                []
            ),

            styles
        )
    )


    # ========================================================
    # WEAKNESSES
    # ========================================================

    story.append(

        Paragraph(

            "15. Improvement Areas",

            heading_style
        )
    )


    story.extend(

        make_bullet_list(

            improvement_result.get(
                "weaknesses",
                []
            ),

            styles
        )
    )


    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    story.append(

        Paragraph(

            "16. Actionable Recommendations",

            heading_style
        )
    )


    recommendations = (
        improvement_result.get(
            "recommendations",
            []
        )
    )


    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        story.append(

            Paragraph(

                f"{index}. "
                f"{safe_text(recommendation)}",

                body_style
            )
        )


    # ========================================================
    # DISCLAIMER
    # ========================================================

    story.append(
        Spacer(
            1,
            15
        )
    )


    story.append(

        Paragraph(

            "<b>Note:</b> This report provides "
            "AI-assisted resume and job compatibility "
            "analysis based on the project's skill "
            "database and semantic similarity model. "
            "The scores should be treated as analytical "
            "guidance rather than a guarantee of "
            "employment or an official ATS evaluation.",

            body_style
        )
    )


    # ========================================================
    # BUILD PDF
    # ========================================================

    document.build(
        story
    )


    buffer.seek(
        0
    )


    return buffer