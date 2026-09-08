import os
import clickhouse_connect
from dotenv import load_dotenv

load_dotenv("../.env")

client = clickhouse_connect.get_client(
    host=os.getenv("CLICKHOUSE_HOST"),
    username=os.getenv("CLICKHOUSE_USER"),
    password=os.getenv("CLICKHOUSE_PASSWORD"),
    secure=True
)

query = """
SELECT
    CASE
        WHEN age < 25 THEN '18-24'
        WHEN age < 35 THEN '25-34'
        WHEN age < 45 THEN '35-44'
        WHEN age < 55 THEN '45-54'
        ELSE '55+'
    END AS age_group,
    uniqExact(viewer_id) AS unique_viewers,
    count() AS events,
    round(avg(completion_rate) * 100, 1) AS avg_completion_percent,
    round(avg(watch_duration_seconds), 0) AS avg_watch_seconds
FROM viewer_events
GROUP BY age_group
ORDER BY age_group
"""

results = client.query(query).result_set

print("\nAge Group Performance")
print("-" * 70)

for row in results:
    print(row)