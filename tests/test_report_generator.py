from io import BytesIO

from src.report_generator import (
    generate_resume_report
)


def create_sample_resume_profile():

    return {
        "name": "John Doe",

        "email": "john.doe@gmail.com",

        "phone": "+91 9876543210",

        "summary": (
            "AI and ML enthusiast with experience "
            "in Python, NLP and machine learning."
        ),

        "education": (
            "Master of Computer Applications "
            "from Anna University."
        ),

        "experience": (
            "Machine Learning Intern "
            "with practical experience in Python."
        ),

        "projects": (
            "AI Resume Intelligence System"
        ),

        "certifications": (
            "Machine Learning Certification"
        ),

        "achievements": "",

        "publications": "",

        "skills": [
            "python",
            "machine learning",
            "nlp",
            "pandas"
        ]
    }


def create_sample_job_profile():

    return {
        "description": (
            "Looking for a Machine Learning Engineer "
            "with Python, machine learning, SQL and "
            "Docker experience."
        ),

        "skills": [
            "python",
            "machine learning",
            "sql",
            "docker"
        ],

        "skill_categories": {
            "programming": [
                "python"
            ],
            "ai": [
                "machine learning"
            ],
            "database": [
                "sql"
            ],
            "devops": [
                "docker"
            ]
        },

        "skill_count": 4
    }


def create_sample_skill_result():

    return {
        "matched_skills": [
            "machine learning",
            "python"
        ],

        "missing_skills": [
            "docker",
            "sql"
        ],

        "additional_skills": [
            "nlp",
            "pandas"
        ],

        "skill_score": 0.50
    }


def create_sample_improvement_result():

    return {
        "improvement_score": 70.0,

        "skill_coverage": {
            "total_job_skills": 4,

            "matched_skills": [
                "machine learning",
                "python"
            ],

            "missing_skills": [
                "docker",
                "sql"
            ],

            "coverage": 0.50
        },

        "strengths": [
            "The resume contains relevant skills.",
            "Projects are present."
        ],

        "weaknesses": [
            "Some job-relevant skills are missing."
        ],

        "recommendations": [
            "Strengthen SQL and Docker skills.",
            "Tailor the resume to the target role."
        ]
    }


def test_generate_resume_report_returns_bytesio():

    resume_profile = create_sample_resume_profile()

    job_profile = create_sample_job_profile()

    skill_result = create_sample_skill_result()

    improvement_result = (
        create_sample_improvement_result()
    )

    report = generate_resume_report(

        resume_profile=resume_profile,

        job_profile=job_profile,

        semantic_score=0.75,

        skill_score=0.50,

        overall_score=0.6625,

        skill_result=skill_result,

        critical_gaps=[
            {
                "skill": "sql",
                "category": "database"
            }
        ],

        improvement_result=improvement_result
    )

    assert isinstance(
        report,
        BytesIO
    )


def test_generate_resume_report_contains_pdf_data():

    resume_profile = create_sample_resume_profile()

    job_profile = create_sample_job_profile()

    skill_result = create_sample_skill_result()

    improvement_result = (
        create_sample_improvement_result()
    )

    report = generate_resume_report(

        resume_profile=resume_profile,

        job_profile=job_profile,

        semantic_score=0.75,

        skill_score=0.50,

        overall_score=0.6625,

        skill_result=skill_result,

        critical_gaps=[],

        improvement_result=improvement_result
    )

    pdf_data = report.getvalue()

    assert isinstance(
        pdf_data,
        bytes
    )

    assert len(pdf_data) > 100

    # Every valid PDF begins with %PDF
    assert pdf_data[:4] == b"%PDF"


def test_generate_resume_report_with_empty_optional_sections():

    resume_profile = {
        "name": "Jane Doe",

        "email": "jane@example.com",

        "phone": "",

        "summary": "",

        "education": "",

        "experience": "",

        "projects": "",

        "certifications": "",

        "achievements": "",

        "publications": "",

        "skills": []
    }

    job_profile = {
        "description": (
            "Looking for a Python developer."
        ),

        "skills": [
            "python"
        ],

        "skill_categories": {
            "programming": [
                "python"
            ]
        },

        "skill_count": 1
    }

    skill_result = {
        "matched_skills": [],

        "missing_skills": [
            "python"
        ],

        "additional_skills": [],

        "skill_score": 0.0
    }

    improvement_result = {
        "improvement_score": 0.0,

        "skill_coverage": {
            "total_job_skills": 1,

            "matched_skills": [],

            "missing_skills": [
                "python"
            ],

            "coverage": 0.0
        },

        "strengths": [],

        "weaknesses": [
            "No professional summary was detected."
        ],

        "recommendations": [
            "Add a professional summary."
        ]
    }

    report = generate_resume_report(

        resume_profile=resume_profile,

        job_profile=job_profile,

        semantic_score=0.20,

        skill_score=0.0,

        overall_score=0.13,

        skill_result=skill_result,

        critical_gaps=[
            {
                "skill": "python",
                "category": "programming"
            }
        ],

        improvement_result=improvement_result
    )

    assert isinstance(
        report,
        BytesIO
    )

    assert report.getvalue()[:4] == b"%PDF"
