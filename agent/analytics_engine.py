import os
import clickhouse_connect
from dotenv import load_dotenv


class AnalyticsEngine:

    def __init__(self):
        load_dotenv("../.env")

    def query(self, sql):
        client = clickhouse_connect.get_client(
            host=os.getenv("CLICKHOUSE_HOST"),
            username=os.getenv("CLICKHOUSE_USER"),
            password=os.getenv("CLICKHOUSE_PASSWORD"),
            secure=True
        )

        try:
            return client.query(sql).result_set
        finally:
            client.close()

    def overview(self):
        return self.query("""
            SELECT
                count() AS total_events,
                uniqExact(viewer_id) AS unique_viewers,
                uniqExact(film_id) AS films,
                round(avg(watch_duration_seconds), 0) AS avg_watch_seconds,
                round(avg(completion_rate) * 100, 1) AS avg_completion_percent
            FROM viewer_events
        """)

    def film_performance(self):
        return self.query("""
            SELECT
                film_id,
                film_title,
                genre,
                count() AS events,
                uniqExact(viewer_id) AS unique_viewers,
                round(avg(watch_duration_seconds), 0) AS avg_watch_seconds,
                round(avg(completion_rate) * 100, 1) AS avg_completion_percent
            FROM viewer_events
            GROUP BY film_id, film_title, genre
            ORDER BY avg_completion_percent DESC
        """)

    def country_performance(self):
        return self.query("""
            SELECT
                country,
                uniqExact(viewer_id) AS unique_viewers,
                count() AS events,
                round(avg(completion_rate) * 100, 1) AS avg_completion_percent,
                round(avg(watch_duration_seconds), 0) AS avg_watch_seconds
            FROM viewer_events
            GROUP BY country
            ORDER BY avg_completion_percent DESC
        """)

    def genre_performance(self):
        return self.query("""
            SELECT
                genre,
                count() AS events,
                uniqExact(viewer_id) AS unique_viewers,
                round(avg(completion_rate) * 100, 1) AS avg_completion_percent,
                round(avg(watch_duration_seconds), 0) AS avg_watch_seconds
            FROM viewer_events
            GROUP BY genre
            ORDER BY avg_completion_percent DESC
        """)

    def device_performance(self):
        return self.query("""
            SELECT
                device,
                uniqExact(viewer_id) AS unique_viewers,
                count() AS events,
                round(avg(completion_rate) * 100, 1) AS avg_completion_percent,
                round(avg(watch_duration_seconds), 0) AS avg_watch_seconds
            FROM viewer_events
            GROUP BY device
            ORDER BY unique_viewers DESC
        """)

    def age_performance(self):
        return self.query("""
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
        """)

    def event_performance(self):
        return self.query("""
            SELECT
                event_type,
                count() AS events,
                uniqExact(viewer_id) AS unique_viewers,
                round(avg(completion_rate) * 100, 1) AS avg_completion_percent,
                round(avg(watch_duration_seconds), 0) AS avg_watch_seconds
            FROM viewer_events
            GROUP BY event_type
            ORDER BY events DESC
        """)

    def country_genre_performance(self):
        return self.query("""
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
        """)
    def activity_over_time(self):
        return self.query("""
            SELECT
                toStartOfHour(event_time) AS hour,
                count() AS events,
                uniqExact(viewer_id) AS unique_viewers
            FROM viewer_events
            GROUP BY hour
            ORDER BY hour
        """)


if __name__ == "__main__":
    engine = AnalyticsEngine()

    print("\nStudioPulse Analytics Engine")
    print("=" * 60)

    print("\nOVERVIEW")
    print(engine.overview())

    print("\nFILM PERFORMANCE")
    for row in engine.film_performance():
        print(row)

    print("\nCOUNTRY PERFORMANCE")
    for row in engine.country_performance():
        print(row)

    print("\nGENRE PERFORMANCE")
    for row in engine.genre_performance():
        print(row)

    print("\nDEVICE PERFORMANCE")
    for row in engine.device_performance():
        print(row)

    print("\nAGE PERFORMANCE")
    for row in engine.age_performance():
        print(row)

    print("\nEVENT PERFORMANCE")
    for row in engine.event_performance():
        print(row)