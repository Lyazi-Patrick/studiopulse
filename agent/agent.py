from google.adk.agents import Agent
from analytics_engine import AnalyticsEngine

_engine = AnalyticsEngine()


def get_overview() -> dict:
    """Get high-level StudioPulse audience metrics: total events, unique
    viewers, number of films, average watch duration, and average
    completion rate across the entire dataset."""
    row = _engine.overview()[0]
    return {
        "total_events": row[0],
        "unique_viewers": row[1],
        "films": row[2],
        "avg_watch_seconds": row[3],
        "avg_completion_percent": row[4],
    }


def get_film_performance() -> list[dict]:
    """Get per-film audience metrics: events, unique viewers, average watch
    duration, and average completion rate for each film in the catalog."""
    rows = _engine.film_performance()
    return [
        {
            "film_id": row[0],
            "film_title": row[1],
            "genre": row[2],
            "events": row[3],
            "unique_viewers": row[4],
            "avg_watch_seconds": row[5],
            "avg_completion_percent": row[6],
        }
        for row in rows
    ]


def get_country_performance() -> list[dict]:
    """Get audience metrics broken down by viewer country: unique viewers,
    events, average completion rate, and average watch duration."""
    rows = _engine.country_performance()
    return [
        {
            "country": row[0],
            "unique_viewers": row[1],
            "events": row[2],
            "avg_completion_percent": row[3],
            "avg_watch_seconds": row[4],
        }
        for row in rows
    ]


def get_genre_performance() -> list[dict]:
    """Get audience metrics broken down by film genre: events, unique
    viewers, average completion rate, and average watch duration."""
    rows = _engine.genre_performance()
    return [
        {
            "genre": row[0],
            "events": row[1],
            "unique_viewers": row[2],
            "avg_completion_percent": row[3],
            "avg_watch_seconds": row[4],
        }
        for row in rows
    ]


def get_device_performance() -> list[dict]:
    """Get audience metrics broken down by viewing device (Mobile, Web,
    Tablet, Smart TV): unique viewers, events, average completion rate,
    and average watch duration."""
    rows = _engine.device_performance()
    return [
        {
            "device": row[0],
            "unique_viewers": row[1],
            "events": row[2],
            "avg_completion_percent": row[3],
            "avg_watch_seconds": row[4],
        }
        for row in rows
    ]


def get_age_group_performance() -> list[dict]:
    """Get audience metrics broken down by viewer age group: unique
    viewers, events, average completion rate, and average watch
    duration."""
    rows = _engine.age_performance()
    return [
        {
            "age_group": row[0],
            "unique_viewers": row[1],
            "events": row[2],
            "avg_completion_percent": row[3],
            "avg_watch_seconds": row[4],
        }
        for row in rows
    ]


def get_event_type_performance() -> list[dict]:
    """Get metrics broken down by viewer event type (watch, pause, exit,
    complete): counts, unique viewers, and average completion rate."""
    rows = _engine.event_performance()
    return [
        {
            "event_type": row[0],
            "events": row[1],
            "unique_viewers": row[2],
            "avg_completion_percent": row[3],
            "avg_watch_seconds": row[4],
        }
        for row in rows
    ]


def get_country_genre_performance() -> list[dict]:
    """Get audience metrics broken down by the combination of country and
    genre: events, unique viewers, average completion rate, and average
    watch duration. Useful for finding regional content preferences."""
    rows = _engine.country_genre_performance()
    return [
        {
            "country": row[0],
            "genre": row[1],
            "events": row[2],
            "unique_viewers": row[3],
            "avg_completion_percent": row[4],
            "avg_watch_seconds": row[5],
        }
        for row in rows
    ]


INSIGHT_INSTRUCTION = """
You are the audience intelligence agent for StudioPulse, a real-time
analytics platform for film and streaming teams.

You have tools that query real StudioPulse audience analytics from
ClickHouse. Use them to investigate the data before answering — call as
many as you need (overview, films, countries, genres, devices, age
groups, event types, country x genre) to find ONE meaningful and
actionable audience pattern.

Rules:
1. Base every claim strictly on data returned by your tools.
2. Include specific numbers in the evidence.
3. Give one practical recommendation a content or streaming team could
   act on.
4. Never claim that one variable causes another — this is observational
   data, not a controlled experiment.
5. If differences are small, say so explicitly rather than overstating
   them.
6. Never invent numbers that were not returned by a tool call.
7. Confidence must be exactly "High", "Medium", or "Low".
8. Your FINAL message must be ONLY valid JSON, no markdown fences, no
   commentary, in exactly this shape:

{
  "insight": "A concise description of the most meaningful pattern.",
  "evidence": "Specific numbers from the dataset supporting the insight.",
  "recommendation": "A practical action a content or streaming team could take.",
  "confidence": "High, Medium, or Low"
}
"""

root_agent = Agent(
    name="studiopulse",
    model="gemini-3.6-flash",
    description="StudioPulse audience intelligence agent",
    instruction=INSIGHT_INSTRUCTION,
    tools=[
        get_overview,
        get_film_performance,
        get_country_performance,
        get_genre_performance,
        get_device_performance,
        get_age_group_performance,
        get_event_type_performance,
        get_country_genre_performance,
    ],
)
