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
    country,
    genre,
    count() AS events,
    uniqExact(viewer_id) AS unique_viewers,
    round(avg(completion_rate) * 100, 1) AS avg_completion_percent,
    round(avg(watch_duration_seconds), 0) AS avg_watch_seconds
FROM viewer_events
GROUP BY country, genre
ORDER BY country, avg_completion_percent DESC
"""

results = client.query(query).result_set

print("\nCountry × Genre Performance")
print("=" * 80)

for row in results:
    print(row)