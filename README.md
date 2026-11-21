# Data Quality Monitoring and Root Cause Dashboard
Python + SQL checks (missing values, duplicates, IQR outliers, PSI drift) on a synthetic orders feed, logged to an auditable `dq_log` table, scheduled as an Airflow DAG in Docker with retries, and exported as a star schema for a Power BI report with a Pareto view of failure causes.
- Data is synthetic, with injected problems (nulls concentrated in the `store` channel, duplicates, outliers, a shifted second batch).
- `docker-compose.yml` is an untested template; `powerbi/DAX_AND_MODEL.md` says how the report is built (the .pbix is not included).
Run: `pip install pandas numpy pytest; python src/gen_data.py; python src/run_checks.py; python src/star.py; pytest`
