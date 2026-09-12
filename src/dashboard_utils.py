import plotly.graph_objects as go


def create_score_gauge(
    score,
    title,
    max_value=100
):
    """
    Create a professional gauge chart.
    """

    score = max(
        0,
        min(
            max_value,
            float(score)
        )
    )

    figure = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={
                "text": title
            },
            gauge={
                "axis": {
                    "range": [
                        0,
                        max_value
                    ]
                }
            }
        )
    )

    figure.update_layout(
        height=280,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    return figure


def create_skill_comparison_chart(
    matched_count,
    missing_count
):
    """
    Create matched vs missing skill chart.
    """

    figure = go.Figure(
        data=[
            go.Bar(
                x=[
                    "Matched Skills",
                    "Missing Skills"
                ],
                y=[
                    matched_count,
                    missing_count
                ],
                text=[
                    matched_count,
                    missing_count
                ],
                textposition="auto"
            )
        ]
    )

    figure.update_layout(
        title="Skill Comparison",
        xaxis_title="Skill Type",
        yaxis_title="Number of Skills",
        height=350
    )

    return figure


def create_job_ranking_chart(
    results
):
    """
    Create a horizontal job ranking chart.
    """

    if not results:
        return None

    job_titles = [
        result["title"]
        for result in results
    ]

    scores = [
        result["overall_score"] * 100
        for result in results
    ]

    figure = go.Figure(
        data=[
            go.Bar(
                x=scores,
                y=job_titles,
                orientation="h",
                text=[
                    f"{score:.1f}%"
                    for score in scores
                ],
                textposition="auto"
            )
        ]
    )

    figure.update_layout(
        title="Job Compatibility Ranking",
        xaxis_title="Compatibility Score (%)",
        yaxis_title="Job",
        xaxis={
            "range": [0, 100]
        },
        height=max(
            350,
            len(results) * 80
        )
    )

    return figure


def create_category_chart(
    category_result
):
    """
    Create skill category comparison chart.
    """

    resume_categories = set(
        category_result.get(
            "resume_categories",
            []
        )
    )

    job_categories = set(
        category_result.get(
            "job_categories",
            []
        )
    )

    categories = sorted(
        resume_categories.union(
            job_categories
        )
    )

    if not categories:
        return None

    resume_values = [
        1 if category in resume_categories
        else 0
        for category in categories
    ]

    job_values = [
        1 if category in job_categories
        else 0
        for category in categories
    ]

    figure = go.Figure()

    figure.add_trace(
        go.Bar(
            name="Resume",
            x=categories,
            y=resume_values
        )
    )

    figure.add_trace(
        go.Bar(
            name="Job",
            x=categories,
            y=job_values
        )
    )

    figure.update_layout(
        title="Skill Category Comparison",
        xaxis_title="Category",
        yaxis_title="Presence",
        barmode="group",
        height=400
    )

    return figure