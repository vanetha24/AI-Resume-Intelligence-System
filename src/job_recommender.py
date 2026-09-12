import pandas as pd


def load_job_database(csv_path="data/jobs.csv"):
    """Load the broad job-role catalog used for automatic recommendations."""
    jobs_df = pd.read_csv(csv_path)

    required_columns = {"category", "title", "description"}
    missing = required_columns - set(jobs_df.columns)

    if missing:
        raise ValueError(
            "jobs.csv is missing columns: " + ", ".join(sorted(missing))
        )

    jobs = []

    for _, row in jobs_df.iterrows():
        category = str(row["category"]).strip()
        title = str(row["title"]).strip()
        description = str(row["description"]).strip()

        if not category or category.lower() == "nan":
            category = "Other"
        if not title or title.lower() == "nan":
            continue
        if not description or description.lower() == "nan":
            continue

        jobs.append({
            "category": category,
            "title": title,
            "description": description,
        })

    return jobs


def get_job_categories(jobs):
    """Return unique job categories in display order."""
    return list(dict.fromkeys(job["category"] for job in jobs))
