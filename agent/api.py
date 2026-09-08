from fastapi import FastAPI
from analytics_engine import AnalyticsEngine
from fastapi.responses import JSONResponse
from agent_runner import get_ai_insight, AIInsightError
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="StudioPulse Analytics API",
    description="Analytics API powered by ClickHouse",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = AnalyticsEngine()


@app.get("/")
def root():
    return {
        "name": "StudioPulse Analytics API",
        "status": "running"
    }


@app.get("/api/overview")
def overview():
    row = engine.overview()[0]

    return {
        "total_events": row[0],
        "unique_viewers": row[1],
        "films": row[2],
        "avg_watch_seconds": row[3],
        "avg_completion_percent": row[4]
    }


@app.get("/api/films")
def films():
    rows = engine.film_performance()

    return [
        {
            "film_id": row[0],
            "film_title": row[1],
            "genre": row[2],
            "events": row[3],
            "unique_viewers": row[4],
            "avg_watch_seconds": row[5],
            "avg_completion_percent": row[6]
        }
        for row in rows
    ]


@app.get("/api/countries")
def countries():
    rows = engine.country_performance()

    return [
        {
            "country": row[0],
            "unique_viewers": row[1],
            "events": row[2],
            "avg_completion_percent": row[3],
            "avg_watch_seconds": row[4]
        }
        for row in rows
    ]


@app.get("/api/genres")
def genres():
    rows = engine.genre_performance()

    return [
        {
            "genre": row[0],
            "events": row[1],
            "unique_viewers": row[2],
            "avg_completion_percent": row[3],
            "avg_watch_seconds": row[4]
        }
        for row in rows
    ]


@app.get("/api/devices")
def devices():
    rows = engine.device_performance()

    return [
        {
            "device": row[0],
            "unique_viewers": row[1],
            "events": row[2],
            "avg_completion_percent": row[3],
            "avg_watch_seconds": row[4]
        }
        for row in rows
    ]


@app.get("/api/age-groups")
def age_groups():
    rows = engine.age_performance()

    return [
        {
            "age_group": row[0],
            "unique_viewers": row[1],
            "events": row[2],
            "avg_completion_percent": row[3],
            "avg_watch_seconds": row[4]
        }
        for row in rows
    ]


@app.get("/api/events")
def events():
    rows = engine.event_performance()

    return [
        {
            "event_type": row[0],
            "events": row[1],
            "unique_viewers": row[2],
            "avg_completion_percent": row[3],
            "avg_watch_seconds": row[4]
        }
        for row in rows
    ]


@app.get("/api/country-genres")
def country_genres():
    rows = engine.country_genre_performance()

    return [
        {
            "country": row[0],
            "genre": row[1],
            "events": row[2],
            "unique_viewers": row[3],
            "avg_completion_percent": row[4],
            "avg_watch_seconds": row[5]
        }
        for row in rows
    ]

@app.get("/api/activity")
def activity():
    rows = engine.activity_over_time()

    return [
        {
            "hour": row[0].isoformat(),
            "events": row[1],
            "unique_viewers": row[2]
        }
        for row in rows
    ]
@app.get("/api/ai-insights")
async def get_ai_insights():
    try:
        return await get_ai_insight()
    except AIInsightError as e:
        return JSONResponse(status_code=503, content={"error": str(e)})