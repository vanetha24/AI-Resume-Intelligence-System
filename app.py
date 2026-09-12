import os
import tempfile

import pandas as pd
import streamlit as st

from src.parser import extract_resume_text
from src.text_cleaner import clean_text

from src.skill_extractor import (
    load_skills,
    group_skills_by_category
)

from src.resume_analyzer import (
    analyze_resume
)

from src.job_analyzer import (
    analyze_job_description
)

from src.embeddings import (
    EmbeddingModel
)

from src.matcher import (
    calculate_semantic_similarity,
    calculate_skill_match,
    calculate_category_match,
    identify_critical_gaps,
    calculate_overall_score
)

from src.recommender import (
    generate_recommendations
)

from src.multi_job_matcher import (
    rank_jobs
)

from src.job_recommender import (
    load_job_database,
    get_job_categories
)

from src.resume_improver import (
    analyze_resume_improvement
)

from src.ats_scorer import (
    calculate_ats_score
)

from src.dashboard_utils import (
    create_score_gauge,
    create_skill_comparison_chart,
    create_job_ranking_chart,
    create_category_chart
)

from src.report_generator import (
    generate_resume_report
)

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        margin-bottom: 25px;
    }

    .section-title {
        font-size: 27px;
        font-weight: 600;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    .info-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 15px;
    }

    .small-text {
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">'
    '🤖 AI-Powered Resume Intelligence'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze resumes, match job descriptions, '
    'identify skill gaps, rank opportunities, '
    'and improve resume relevance.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# LOAD SKILL DATABASE
# ============================================================

try:

    skills_df = load_skills(
        "data/skills.csv"
    )

except Exception as error:

    st.error(
        "Unable to load the skill database."
    )

    st.exception(error)

    st.stop()


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

@st.cache_resource
def load_embedding_model():

    return EmbeddingModel()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "⚙️ Analysis"
    )

    analysis_mode = st.radio(
        "Select Mode",
        [
            "Single Job Analysis",
            "Multi-Job Recommendation",
            "Recommended Jobs"
        ]
    )

    st.markdown("---")

    st.subheader(
        "System Features"
    )

    st.write(
        "📄 Resume Parsing"
    )

    st.write(
        "🧠 NLP Skill Extraction"
    )

    st.write(
        "🔢 Semantic Embeddings"
    )

    st.write(
        "🎯 Job Matching"
    )

    st.write(
        "📊 Skill Gap Analysis"
    )

    st.write(
        "🏆 Job Ranking"
    )

    st.write(
        "✨ Resume Improvement"
    )


# ============================================================
# RESUME UPLOAD
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📄 Upload Your Resume'
    '</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload PDF or DOCX",
    type=[
        "pdf",
        "docx"
    ]
)


if uploaded_file is None:

    st.info(
        "Upload your resume to start the analysis."
    )

    st.stop()


# ============================================================
# TEMPORARY FILE
# ============================================================

file_extension = os.path.splitext(
    uploaded_file.name
)[1]


with tempfile.NamedTemporaryFile(
    delete=False,
    suffix=file_extension
) as temp_file:

    temp_file.write(
        uploaded_file.getbuffer()
    )

    temp_file_path = temp_file.name


# ============================================================
# RESUME EXTRACTION
# ============================================================

try:

    resume_text = extract_resume_text(
        temp_file_path
    )

    resume_text = clean_text(
        resume_text
    )

except Exception as error:

    st.error(
        "Unable to process the resume."
    )

    st.exception(error)

    try:
        os.unlink(
            temp_file_path
        )
    except Exception:
        pass

    st.stop()


try:

    os.unlink(
        temp_file_path
    )

except Exception:

    pass


if not resume_text.strip():

    st.error(
        "No readable text was found in the resume."
    )

    st.stop()


# ============================================================
# RESUME ANALYSIS
# ============================================================

try:

    resume_profile = analyze_resume(
        resume_text,
        skills_df
    )

except Exception as error:

    st.error(
        "Resume analysis failed."
    )

    st.exception(error)

    st.stop()


# ============================================================
# RESUME SUMMARY CARDS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🧠 Resume Intelligence'
    '</div>',
    unsafe_allow_html=True
)


resume_col1, resume_col2, resume_col3, resume_col4 = (
    st.columns(4)
)


with resume_col1:

    st.metric(
        "Skills Detected",
        len(
            resume_profile.get(
                "skills",
                []
            )
        )
    )


with resume_col2:

    st.metric(
        "Projects",
        "Yes"
        if resume_profile.get(
            "projects"
        )
        else "No"
    )


with resume_col3:

    st.metric(
        "Experience",
        "Yes"
        if resume_profile.get(
            "experience"
        )
        else "No"
    )


with resume_col4:

    st.metric(
        "Education",
        "Yes"
        if resume_profile.get(
            "education"
        )
        else "No"
    )


# ============================================================
# RESUME DETAILS
# ============================================================

with st.expander(
    "🔎 View Resume Intelligence"
):

    personal_col1, personal_col2 = (
        st.columns(2)
    )

    with personal_col1:

        st.write(
            "**Name:**",
            resume_profile.get(
                "name"
            ) or "Not detected"
        )

        st.write(
            "**Email:**",
            resume_profile.get(
                "email"
            ) or "Not detected"
        )

        st.write(
            "**Phone:**",
            resume_profile.get(
                "phone"
            ) or "Not detected"
        )

    with personal_col2:

        st.write(
            "**Skills:**"
        )

        skills = resume_profile.get(
            "skills",
            []
        )

        if skills:

            st.write(
                ", ".join(
                    skill.title()
                    for skill in skills
                )
            )

        else:

            st.write(
                "No skills detected."
            )


# ============================================================
# EMBEDDING MODEL
# ============================================================

embedding_model = load_embedding_model()


# ============================================================
# SINGLE JOB MODE
# ============================================================

if analysis_mode == "Single Job Analysis":

    st.markdown(
        '<div class="section-title">'
        '💼 Target Job'
        '</div>',
        unsafe_allow_html=True
    )

    job_description = st.text_area(
        "Paste the Job Description",
        height=280,
        placeholder=(
            "Paste the complete job description "
            "here..."
        )
    )


    if not job_description.strip():

        st.info(
            "Paste a job description to begin "
            "job matching."
        )

        st.stop()


    # ========================================================
    # JOB ANALYSIS
    # ========================================================

    job_profile = analyze_job_description(
        job_description,
        skills_df
    )


    # ========================================================
    # JOB SKILLS
    # ========================================================

    st.subheader(
        "🎯 Detected Job Skills"
    )

    job_skills = job_profile[
        "skills"
    ]

    if job_skills:

        st.write(
            ", ".join(
                skill.title()
                for skill in job_skills
            )
        )

    else:

        st.warning(
            "No skills were detected from this job description."
        )


    # ========================================================
    # SKILL MATCH
    # ========================================================

    skill_result = calculate_skill_match(
        resume_profile["skills"],
        job_profile["skills"]
    )


    matched_skills = skill_result[
        "matched_skills"
    ]

    missing_skills = skill_result[
        "missing_skills"
    ]

    additional_skills = skill_result[
        "additional_skills"
    ]

    skill_score = skill_result[
        "skill_score"
    ]


    # ========================================================
    # CATEGORY MATCH
    # ========================================================

    category_result = calculate_category_match(
        resume_profile["skills"],
        job_profile["skills"],
        skills_df
    )


    # ========================================================
    # EMBEDDINGS
    # ========================================================

    with st.spinner(
        "Calculating semantic similarity..."
    ):

        resume_embedding = (
            embedding_model.encode(
                resume_text
            )
        )

        job_embedding = (
            embedding_model.encode(
                job_description
            )
        )


    semantic_score = (
        calculate_semantic_similarity(
            resume_embedding,
            job_embedding
        )
    )


    # ========================================================
    # OVERALL MATCH
    # ========================================================

    overall_score = (
        calculate_overall_score(
            semantic_score,
            skill_score
        )
    )

    # ========================================================
    # ATS COMPATIBILITY ANALYSIS
    # ========================================================

    with st.spinner(
        "Calculating ATS compatibility score..."
    ):
        ats_result = calculate_ats_score(
            resume_profile=resume_profile,
            job_profile=job_profile,
            semantic_score=semantic_score,
            embedding_model=embedding_model,
            resume_text=resume_text
        )

    ats_score = ats_result["ats_score"]
    ats_score_percentage = ats_result[
        "ats_score_percentage"
    ]


    # ========================================================
    # MAIN SCORE DASHBOARD
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📊 Job Compatibility Dashboard'
        '</div>',
        unsafe_allow_html=True
    )


    score1, score2, score3 = (
        st.columns(3)
    )


    with score1:

        st.plotly_chart(
            create_score_gauge(
                semantic_score * 100,
                "Semantic Similarity"
            ),
            use_container_width=True
        )


    with score2:

        st.plotly_chart(
            create_score_gauge(
                skill_score * 100,
                "Skill Match"
            ),
            use_container_width=True
        )


    with score3:

        st.plotly_chart(
            create_score_gauge(
                overall_score * 100,
                "Overall Match"
            ),
            use_container_width=True
        )


    st.caption(
        "Overall Match = 65% Semantic Similarity "
        "+ 35% Explicit Skill Match"
    )


    # ========================================================
    # ATS COMPATIBILITY DASHBOARD
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🤖 ATS Compatibility Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    ats_col1, ats_col2 = st.columns([1, 2])

    with ats_col1:
        st.metric(
            "ATS Compatibility Score",
            f"{ats_score:.1f}/100"
        )

        if ats_score >= 80:
            st.success(
                "Strong ATS compatibility"
            )
        elif ats_score >= 60:
            st.warning(
                "Moderate ATS compatibility"
            )
        else:
            st.error(
                "Low ATS compatibility"
            )

    with ats_col2:
        st.plotly_chart(
            create_score_gauge(
                ats_score_percentage,
                "ATS Compatibility"
            ),
            use_container_width=True
        )

    st.caption(
        "ATS Compatibility Score is a transparent, project-specific "
        "estimate based on job keywords, semantic relevance, "
        "resume completeness, relevance, and parseability. "
        "It is not an official score from a specific ATS vendor."
    )


    # ========================================================
    # ATS SCORE BREAKDOWN
    # ========================================================

    st.subheader(
        "📊 ATS Score Breakdown"
    )

    breakdown = ats_result.get(
        "score_breakdown",
        {}
    )

    breakdown_data = []

    breakdown_labels = {
        "keyword_score": "Keyword Match",
        "semantic_score": "Semantic Relevance",
        "section_score": "Section Completeness",
        "experience_score": "Experience Relevance",
        "education_score": "Education Relevance",
        "project_score": "Project Relevance",
        "parseability_score": "ATS Parseability"
    }

    breakdown_weights = {
        "keyword_score": 30,
        "semantic_score": 25,
        "section_score": 15,
        "experience_score": 10,
        "education_score": 5,
        "project_score": 5,
        "parseability_score": 10
    }

    for key, label in breakdown_labels.items():
        value = float(
            breakdown.get(key, 0)
        )

        weight = breakdown_weights[key]

        breakdown_data.append({
            "Component": label,
            "Score": f"{value:.1f}/{weight}",
            "Percentage": f"{(value / weight * 100) if weight else 0:.1f}%"
        })

    if breakdown_data:
        st.dataframe(
            pd.DataFrame(breakdown_data),
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # ATS KEYWORD ANALYSIS
    # ========================================================

    ats_keyword_result = ats_result.get(
        "keyword_result",
        {}
    )

    st.subheader(
        "🔑 ATS Keyword Analysis"
    )

    keyword_col1, keyword_col2, keyword_col3 = st.columns(3)

    with keyword_col1:
        st.metric(
            "Required Keywords",
            ats_keyword_result.get(
                "total_job_skills",
                len(job_skills)
            )
        )

    with keyword_col2:
        st.metric(
            "Matched Keywords",
            len(
                ats_keyword_result.get(
                    "matched_skills",
                    []
                )
            )
        )

    with keyword_col3:
        keyword_coverage = ats_keyword_result.get(
            "coverage",
            0
        )

        st.metric(
            "Keyword Coverage",
            f"{keyword_coverage * 100:.1f}%"
        )

    keyword_matched = ats_keyword_result.get(
        "matched_skills",
        []
    )

    keyword_missing = ats_keyword_result.get(
        "missing_skills",
        []
    )

    ats_keyword_match_col, ats_keyword_missing_col = st.columns(2)

    with ats_keyword_match_col:
        st.write("**Matched Job Keywords**")

        if keyword_matched:
            st.success(
                ", ".join(
                    skill.title()
                    for skill in keyword_matched
                )
            )
        else:
            st.write("None detected")

    with ats_keyword_missing_col:
        st.write("**Missing Job Keywords**")

        if keyword_missing:
            st.warning(
                ", ".join(
                    skill.title()
                    for skill in keyword_missing
                )
            )
        else:
            st.success("No missing job keywords detected")


    # ========================================================
    # ATS SECTION ANALYSIS
    # ========================================================

    st.subheader(
        "📋 ATS Resume Section Analysis"
    )

    section_result = ats_result.get(
        "section_result",
        {}
    )

    section_data = []

    sections = section_result.get(
        "sections",
        {}
    )

    if isinstance(sections, dict):
        for section_name, section_value in sections.items():
            if isinstance(section_value, bool):
                status = "Present" if section_value else "Missing"
            else:
                status = str(section_value)

            section_data.append({
                "Section": str(section_name).title(),
                "Status": status
            })

    if section_data:
        st.dataframe(
            pd.DataFrame(section_data),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(
            "Section-level ATS details are not available."
        )


    # ========================================================
    # ATS ISSUES
    # ========================================================

    st.subheader(
        "⚠️ ATS Issues"
    )

    ats_issues = ats_result.get(
        "issues",
        []
    )

    if ats_issues:
        for issue in ats_issues:
            st.warning(issue)
    else:
        st.success(
            "No major ATS compatibility issues were detected."
        )


    # ========================================================
    # ATS RECOMMENDATIONS
    # ========================================================

    st.subheader(
        "💡 ATS Recommendations"
    )

    ats_recommendations = ats_result.get(
        "recommendations",
        []
    )

    if ats_recommendations:
        for index, recommendation in enumerate(
            ats_recommendations,
            start=1
        ):
            st.info(
                f"**{index}.** {recommendation}"
            )
    else:
        st.success(
            "No additional ATS recommendations."
        )


    # ========================================================
    # SKILL COMPARISON
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '🔑 Skill Analysis'
        '</div>',
        unsafe_allow_html=True
    )


    skill_chart_col, skill_details_col = (
        st.columns([1, 1])
    )


    with skill_chart_col:

        st.plotly_chart(
            create_skill_comparison_chart(
                len(matched_skills),
                len(missing_skills)
            ),
            use_container_width=True
        )


    with skill_details_col:

        st.subheader(
            "Skill Coverage"
        )

        total_job_skills = len(
            job_skills
        )

        if total_job_skills:

            coverage = (
                len(matched_skills)
                /
                total_job_skills
            )

        else:

            coverage = 0


        st.metric(
            "Job Skill Coverage",
            f"{coverage * 100:.1f}%"
        )


        st.write(
            f"✅ Matched: {len(matched_skills)}"
        )

        st.write(
            f"❌ Missing: {len(missing_skills)}"
        )


    # ========================================================
    # MATCHED / MISSING / ADDITIONAL
    # ========================================================

    matched_col, missing_col, additional_col = (
        st.columns(3)
    )


    with matched_col:

        st.subheader(
            "✅ Matched"
        )

        if matched_skills:

            for skill in matched_skills:

                st.success(
                    skill.title()
                )

        else:

            st.write(
                "None"
            )


    with missing_col:

        st.subheader(
            "❌ Missing"
        )

        if missing_skills:

            for skill in missing_skills:

                st.error(
                    skill.title()
                )

        else:

            st.success(
                "None"
            )


    with additional_col:

        st.subheader(
            "➕ Additional"
        )

        if additional_skills:

            for skill in additional_skills:

                st.info(
                    skill.title()
                )

        else:

            st.write(
                "None"
            )


    # ========================================================
    # CATEGORY CHART
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        '📚 Skill Category Analysis'
        '</div>',
        unsafe_allow_html=True
    )


    category_chart = create_category_chart(
        category_result
    )


    if category_chart:

        st.plotly_chart(
            category_chart,
            use_container_width=True
        )


    # ========================================================
    # CRITICAL GAPS
    # ========================================================

    critical_gaps = identify_critical_gaps(
        missing_skills,
        skills_df
    )


    st.subheader(
        "🚨 Critical Skill Gaps"
    )


    if critical_gaps:

        for gap in critical_gaps:

            st.warning(
                f"{gap['skill'].title()} "
                f"({gap['category'].title()})"
            )

    else:

        st.success(
            "No major critical skill gaps detected."
        )


    # ========================================================
    # MATCH RECOMMENDATIONS
    # ========================================================

    st.subheader(
        "💡 Job Match Recommendations"
    )


    recommendations = (
        generate_recommendations(
            missing_skills,
            semantic_score,
            skill_score
        )
    )


    for index, recommendation in enumerate(
        recommendations,
        start=1
    ):

        st.info(
            f"**{index}.** {recommendation}"
        )


    # ========================================================
    # RESUME IMPROVEMENT INTELLIGENCE
    # ========================================================
    st.markdown("---")
    st.markdown(
        '<div class="section-title">'
        '✨ Resume Improvement Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    # Calculate the improvement analysis before displaying it.
    # This section is independent from PDF generation, so a PDF
    # error cannot prevent the improvement results from appearing.
    try:
        improvement_result = analyze_resume_improvement(
            resume_profile,
            job_profile
        )

        improvement_score = float(
            improvement_result.get(
                "improvement_score", 0
            )
        )

        skill_coverage = improvement_result.get(
            "skill_coverage", {}
        )

        strengths = improvement_result.get(
            "strengths", []
        )

        weaknesses = improvement_result.get(
            "weaknesses", []
        )

        improvement_recommendations = improvement_result.get(
            "recommendations", []
        )

        # ---------------- Resume Score ----------------
        improvement_col1, improvement_col2 = st.columns([1, 2])

        with improvement_col1:
            st.metric(
                "Resume Improvement Score",
                f"{improvement_score:.1f}/100"
            )

            if improvement_score >= 80:
                st.success("Strong resume alignment")
            elif improvement_score >= 60:
                st.info("Good foundation with some areas to improve")
            elif improvement_score >= 40:
                st.warning("Several areas need improvement")
            else:
                st.error("Resume needs significant improvement")

        with improvement_col2:
            st.plotly_chart(
                create_score_gauge(
                    improvement_score,
                    "Resume Improvement Score"
                ),
                use_container_width=True
            )

        st.caption(
            "This is a project-specific improvement score based on "
            "job-skill coverage and detected resume sections. "
            "It is not an official ATS score."
        )

        # ---------------- Keyword Coverage ----------------
        st.subheader("🔑 Job Skill Keyword Coverage")

        required_skills = int(
            skill_coverage.get(
                "total_job_skills", 0
            )
        )

        covered_skills = skill_coverage.get(
            "matched_skills", []
        ) or []

        missing_job_skills = skill_coverage.get(
            "missing_skills", []
        ) or []

        coverage_value = float(
            skill_coverage.get(
                "coverage", 0
            )
        )

        coverage_col1, coverage_col2, coverage_col3 = st.columns(3)

        with coverage_col1:
            st.metric(
                "Required Job Skills",
                required_skills
            )

        with coverage_col2:
            st.metric(
                "Matched Skills",
                len(covered_skills)
            )

        with coverage_col3:
            st.metric(
                "Skill Coverage",
                f"{coverage_value * 100:.1f}%"
            )

        if missing_job_skills:
            st.write("**Skills to consider strengthening:**")
            st.write(
                ", ".join(
                    skill.title()
                    for skill in missing_job_skills
                )
            )
        else:
            st.success(
                "All detected job skills are already present in the resume."
            )

        # ---------------- Resume Section Analysis ----------------
        st.subheader("📋 Resume Section Analysis")

        section_rows = []

        section_definitions = [
            ("Professional Summary", "summary"),
            ("Education", "education"),
            ("Experience", "experience"),
            ("Projects", "projects"),
            ("Certifications", "certifications"),
            ("Achievements", "achievements"),
            ("Publications", "publications")
        ]

        for section_name, section_key in section_definitions:
            section_value = resume_profile.get(
                section_key,
                ""
            )

            has_section = bool(
                isinstance(section_value, str)
                and section_value.strip()
            )

            section_rows.append({
                "Section": section_name,
                "Status": "Detected" if has_section else "Not detected"
            })

        section_df = pd.DataFrame(section_rows)
        st.dataframe(
            section_df,
            use_container_width=True,
            hide_index=True
        )

        # ---------------- Strengths ----------------
        st.subheader("💪 Resume Strengths")

        if strengths:
            for strength in strengths:
                st.success(str(strength))
        else:
            st.info("No specific strengths were detected.")

        # ---------------- Weaknesses ----------------
        st.subheader("⚠️ Improvement Areas")

        if weaknesses:
            for weakness in weaknesses:
                st.warning(str(weakness))
        else:
            st.success("No major improvement areas were detected.")

        # ---------------- Actionable Recommendations ----------------
        st.subheader("📝 Actionable Recommendations")

        if improvement_recommendations:
            for index, recommendation in enumerate(
                improvement_recommendations,
                start=1
            ):
                st.info(
                    f"**{index}.** {recommendation}"
                )
        else:
            st.success(
                "No additional recommendations were generated."
            )

    except Exception as error:
        st.error(
            "Unable to calculate Resume Improvement Intelligence."
        )
        st.exception(error)

    # ========================================================
    # DOWNLOAD PDF REPORT
    # ========================================================
    st.markdown("---")
    st.subheader("📄 Download Resume Analysis Report")

    st.write(
        "Generate a professional PDF containing your resume analysis, "
        "job compatibility, skill gaps, and improvement recommendations."
    )

    try:
        report_buffer = generate_resume_report(
            resume_profile=resume_profile,
            job_profile=job_profile,
            semantic_score=semantic_score,
            skill_score=skill_score,
            overall_score=overall_score,
            skill_result=skill_result,
            critical_gaps=critical_gaps,
            improvement_result=improvement_result
        )

        candidate_name = (
            resume_profile.get("name")
            or "candidate"
        )

        safe_name = (
            candidate_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        st.download_button(
            label="📥 Download PDF Report",
            data=report_buffer.getvalue(),
            file_name=(
                f"{safe_name}_resume_analysis_report.pdf"
            ),
            mime="application/pdf",
            type="primary"
        )

    except Exception as error:
        st.error(
            "Unable to generate the PDF report."
        )
        st.exception(error)


# ============================================================
# MULTI-JOB MODE
# ============================================================

elif analysis_mode == "Multi-Job Recommendation":

    st.markdown(
        '<div class="section-title">'
        '🏆 Multi-Job Recommendation'
        '</div>',
        unsafe_allow_html=True
    )


    st.write(
        "Enter multiple job descriptions and "
        "the system will rank them according "
        "to resume-job compatibility."
    )


    number_of_jobs = st.number_input(
        "Number of Jobs",
        min_value=2,
        max_value=10,
        value=3,
        step=1
    )


    jobs = []


    # ========================================================
    # JOB INPUT
    # ========================================================

    for index in range(
        int(number_of_jobs)
    ):

        st.subheader(
            f"Job {index + 1}"
        )


        title = st.text_input(
            f"Job Title {index + 1}",
            key=f"title_{index}"
        )


        description = st.text_area(
            f"Job Description {index + 1}",
            height=180,
            key=f"description_{index}"
        )


        jobs.append({
            "title":
                title.strip()
                if title.strip()
                else f"Job {index + 1}",

            "description":
                description
        })


    # ========================================================
    # RANK JOBS
    # ========================================================

    if st.button(
        "🚀 Analyze and Rank Jobs",
        type="primary"
    ):

        valid_jobs = [
            job
            for job in jobs
            if job["description"].strip()
        ]


        if not valid_jobs:

            st.warning(
                "Please enter at least one "
                "job description."
            )

            st.stop()


        with st.spinner(
            "Analyzing all jobs..."
        ):

            results = rank_jobs(
                resume_text,
                resume_profile["skills"],
                valid_jobs,
                skills_df,
                embedding_model
            )


        if not results:

            st.warning(
                "No jobs could be analyzed."
            )

            st.stop()


        # ====================================================
        # BEST JOB
        # ====================================================

        best_job = results[0]


        st.markdown(
            '<div class="section-title">'
            '🏆 Recommended Job'
            '</div>',
            unsafe_allow_html=True
        )


        st.success(
            f"### {best_job['title']}"
        )


        best_col1, best_col2 = (
            st.columns(2)
        )


        with best_col1:

            st.metric(
                "Overall Match",
                f"{best_job['overall_score'] * 100:.1f}%"
            )


        with best_col2:

            st.metric(
                "Skill Match",
                f"{best_job['skill_score'] * 100:.1f}%"
            )


        # ====================================================
        # JOB RANKING CHART
        # ====================================================

        st.subheader(
            "📊 Job Compatibility Ranking"
        )


        ranking_chart = (
            create_job_ranking_chart(
                results
            )
        )


        if ranking_chart:

            st.plotly_chart(
                ranking_chart,
                use_container_width=True
            )


        # ====================================================
        # RANKING TABLE
        # ====================================================

        ranking_data = []


        for result in results:

            ranking_data.append({

                "Rank":
                    result["rank"],

                "Job":
                    result["title"],

                "Overall Match":
                    f"{result['overall_score'] * 100:.1f}%",

                "Semantic":
                    f"{result['semantic_score'] * 100:.1f}%",

                "Skill Match":
                    f"{result['skill_score'] * 100:.1f}%",

                "Matched":
                    len(
                        result[
                            "matched_skills"
                        ]
                    ),

                "Missing":
                    len(
                        result[
                            "missing_skills"
                        ]
                    )
            })


        ranking_df = pd.DataFrame(
            ranking_data
        )


        st.dataframe(
            ranking_df,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # DETAILS
        # ====================================================

        st.subheader(
            "🔎 Detailed Job Analysis"
        )


        for result in results:

            with st.expander(
                f"#{result['rank']} "
                f"{result['title']} — "
                f"{result['overall_score'] * 100:.1f}%"
            ):

                detail1, detail2 = (
                    st.columns(2)
                )


                with detail1:

                    st.metric(
                        "Semantic Similarity",
                        f"{result['semantic_score'] * 100:.1f}%"
                    )

                    st.metric(
                        "Skill Match",
                        f"{result['skill_score'] * 100:.1f}%"
                    )


                with detail2:

                    st.write(
                        "**Matched Skills**"
                    )

                    if result[
                        "matched_skills"
                    ]:

                        st.write(
                            ", ".join(
                                skill.title()
                                for skill in result[
                                    "matched_skills"
                                ]
                            )
                        )

                    else:

                        st.write(
                            "None"
                        )


                    st.write(
                        "**Missing Skills**"
                    )

                    if result[
                        "missing_skills"
                    ]:

                        st.write(
                            ", ".join(
                                skill.title()
                                for skill in result[
                                    "missing_skills"
                                ]
                            )
                        )

                    else:

                        st.write(
                            "None"
                        )


                    st.write(
                        "**Additional Resume Skills**"
                    )

                    if result[
                        "additional_skills"
                    ]:

                        st.write(
                            ", ".join(
                                skill.title()
                                for skill in result[
                                    "additional_skills"
                                ]
                            )
                        )

                    else:

                        st.write(
                            "None"
                        )


# ============================================================
# RECOMMENDED JOBS MODE
# ============================================================

else:

    st.markdown(
        '<div class="section-title">'
        '🎯 Recommended Jobs for Your Resume'
        '</div>',
        unsafe_allow_html=True
    )

    st.write(
        "This module compares your complete resume with a broad "
        "job-role catalog and automatically recommends the roles "
        "that best match your skills, projects, education and "
        "overall resume content."
    )

    st.info(
        "This feature recommends job roles, not live vacancies. "
        "It does not require a paid API."
    )

    try:
        job_database = load_job_database(
            "data/jobs.csv"
        )
    except Exception as error:
        st.error(
            "Unable to load the job-role database."
        )
        st.exception(error)
        st.stop()

    if not job_database:
        st.warning(
            "No job roles are available."
        )
        st.stop()

    # ------------------------------------------------------------
    # JOB CATALOG OVERVIEW
    # ------------------------------------------------------------

    categories = get_job_categories(
        job_database
    )

    overview_col1, overview_col2, overview_col3 = (
        st.columns(3)
    )

    with overview_col1:
        st.metric(
            "Job Roles Analyzed",
            len(job_database)
        )

    with overview_col2:
        st.metric(
            "Career Categories",
            len(categories)
        )

    with overview_col3:
        st.metric(
            "Resume Skills Detected",
            len(
                resume_profile.get(
                    "skills",
                    []
                )
            )
        )

    with st.expander(
        "📚 View Job Categories"
    ):
        category_counts = (
            pd.DataFrame(
                [
                    {
                        "Category": category,
                        "Roles": sum(
                            1
                            for job in job_database
                            if job["category"] == category
                        )
                    }
                    for category in categories
                ]
            )
        )

        st.dataframe(
            category_counts,
            use_container_width=True,
            hide_index=True
        )

    # ------------------------------------------------------------
    # NUMBER OF RECOMMENDATIONS
    # ------------------------------------------------------------

    top_n = st.slider(
        "Number of recommended roles",
        min_value=5,
        max_value=min(15, len(job_database)),
        value=min(8, len(job_database)),
        step=1
    )

    # ------------------------------------------------------------
    # RUN RECOMMENDATION
    # ------------------------------------------------------------

    if st.button(
        "🚀 Recommend Jobs for My Resume",
        type="primary"
    ):

        with st.spinner(
            "Analyzing your resume against all job roles..."
        ):

            recommendation_results = rank_jobs(
                resume_text,
                resume_profile["skills"],
                job_database,
                skills_df,
                embedding_model
            )

        # Map title -> category because rank_jobs returns
        # the title and scores while the database stores category.
        category_map = {
            job["title"]: job["category"]
            for job in job_database
        }

        for result in recommendation_results:
            result["category"] = category_map.get(
                result["title"],
                "Other"
            )

        recommendation_results = (
            recommendation_results[:int(top_n)]
        )

        if not recommendation_results:
            st.warning(
                "No job roles could be analyzed."
            )
            st.stop()

        # --------------------------------------------------------
        # BEST RECOMMENDED ROLE
        # --------------------------------------------------------

        best_job = recommendation_results[0]

        st.markdown(
            '<div class="section-title">'
            '🏆 Best Recommended Job Role'
            '</div>',
            unsafe_allow_html=True
        )

        st.success(
            f"### {best_job['title']}"
        )

        st.caption(
            f"Career Category: {best_job['category']}"
        )

        best_col1, best_col2, best_col3 = (
            st.columns(3)
        )

        with best_col1:
            st.metric(
                "Compatibility",
                f"{best_job['overall_score'] * 100:.1f}%"
            )

        with best_col2:
            st.metric(
                "Semantic Relevance",
                f"{best_job['semantic_score'] * 100:.1f}%"
            )

        with best_col3:
            st.metric(
                "Skill Match",
                f"{best_job['skill_score'] * 100:.1f}%"
            )

        st.caption(
            "Compatibility = 65% semantic similarity + "
            "35% explicit skill match."
        )

        # --------------------------------------------------------
        # RANKING CHART
        # --------------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '📊 Recommended Job Ranking'
            '</div>',
            unsafe_allow_html=True
        )

        ranking_chart = create_job_ranking_chart(
            recommendation_results
        )

        if ranking_chart:
            st.plotly_chart(
                ranking_chart,
                use_container_width=True
            )

        # --------------------------------------------------------
        # RANKING TABLE
        # --------------------------------------------------------

        ranking_data = []

        for result in recommendation_results:

            ranking_data.append({
                "Rank": result["rank"],
                "Job Role": result["title"],
                "Category": result["category"],
                "Compatibility": (
                    f"{result['overall_score'] * 100:.1f}%"
                ),
                "Semantic": (
                    f"{result['semantic_score'] * 100:.1f}%"
                ),
                "Skill Match": (
                    f"{result['skill_score'] * 100:.1f}%"
                ),
                "Matched Skills": len(
                    result["matched_skills"]
                ),
                "Missing Skills": len(
                    result["missing_skills"]
                )
            })

        ranking_df = pd.DataFrame(
            ranking_data
        )

        st.dataframe(
            ranking_df,
            use_container_width=True,
            hide_index=True
        )

        # --------------------------------------------------------
        # TOP CAREER CATEGORIES
        # --------------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '🧭 Recommended Career Areas'
            '</div>',
            unsafe_allow_html=True
        )

        category_scores = {}

        for result in recommendation_results:

            category = result["category"]

            category_scores.setdefault(
                category,
                []
            )

            category_scores[
                category
            ].append(
                result["overall_score"]
            )

        category_summary = []

        for category, scores in category_scores.items():

            category_summary.append({
                "Category": category,
                "Average Match": (
                    sum(scores) / len(scores) * 100
                ),
                "Recommended Roles": len(scores)
            })

        category_summary.sort(
            key=lambda item:
                item["Average Match"],
            reverse=True
        )

        category_df = pd.DataFrame(
            category_summary
        )

        if not category_df.empty:

            category_df[
                "Average Match"
            ] = category_df[
                "Average Match"
            ].map(
                lambda value:
                    f"{value:.1f}%"
            )

            st.dataframe(
                category_df,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------------------------
        # WHY EACH ROLE WAS RECOMMENDED
        # --------------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '🔎 Why These Jobs Were Recommended'
            '</div>',
            unsafe_allow_html=True
        )

        for result in recommendation_results:

            score = (
                result["overall_score"] * 100
            )

            with st.expander(
                f"#{result['rank']} "
                f"{result['title']} — "
                f"{score:.1f}%"
            ):

                st.caption(
                    f"Category: {result['category']}"
                )

                detail1, detail2 = (
                    st.columns(2)
                )

                with detail1:

                    st.metric(
                        "Compatibility",
                        f"{score:.1f}%"
                    )

                    st.metric(
                        "Semantic Relevance",
                        f"{result['semantic_score'] * 100:.1f}%"
                    )

                    st.metric(
                        "Skill Match",
                        f"{result['skill_score'] * 100:.1f}%"
                    )

                with detail2:

                    st.write(
                        "**Matched Skills**"
                    )

                    if result[
                        "matched_skills"
                    ]:

                        st.success(
                            ", ".join(
                                skill.title()
                                for skill in result[
                                    "matched_skills"
                                ]
                            )
                        )

                    else:

                        st.write(
                            "No explicit skills matched."
                        )

                    st.write(
                        "**Skills to Develop**"
                    )

                    if result[
                        "missing_skills"
                    ]:

                        st.warning(
                            ", ".join(
                                skill.title()
                                for skill in result[
                                    "missing_skills"
                                ]
                            )
                        )

                    else:

                        st.success(
                            "No missing skills detected."
                        )

                    if result[
                        "additional_skills"
                    ]:

                        st.write(
                            "**Additional Resume Skills**"
                        )

                        st.info(
                            ", ".join(
                                skill.title()
                                for skill in result[
                                    "additional_skills"
                                ]
                            )
                        )

        # --------------------------------------------------------
        # CAREER DIRECTION
        # --------------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            '💡 Career Direction'
            '</div>',
            unsafe_allow_html=True
        )

        top_score = (
            best_job["overall_score"] * 100
        )

        if top_score >= 80:

            st.success(
                f"Your resume shows strong alignment "
                f"with **{best_job['title']}**. "
                f"This is currently your strongest "
                f"recommended role."
            )

        elif top_score >= 65:

            st.info(
                f"**{best_job['title']}** is a promising "
                f"career target. Strengthening the missing "
                f"skills shown above could improve your "
                f"alignment."
            )

        elif top_score >= 50:

            st.warning(
                f"Your resume has moderate alignment "
                f"with **{best_job['title']}**. "
                f"Consider strengthening relevant skills "
                f"and projects."
            )

        else:

            st.warning(
                "The current resume has limited alignment "
                "with the available job roles. Consider "
                "building more role-specific skills and "
                "projects."
            )

    else:

        st.info(
            "Click **Recommend Jobs for My Resume** "
            "to compare your resume with all available "
            "job roles."
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "AI-Powered Resume Intelligence and Job Matching System"
)

st.caption(
    "Built with Python • NLP • Sentence Transformers • "
    "Semantic Similarity • Streamlit"
)