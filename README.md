# StudioPulse

**Real-time audience intelligence for film and streaming teams.**

StudioPulse turns raw viewer-event data into evidence-based, actionable
audience insights. It ingests streaming/viewing events into ClickHouse,
computes audience analytics with a Python analytics engine, exposes them
through a FastAPI backend, visualizes them in a React dashboard, and uses
a Gemini-powered agent to interpret the analytics and surface one
grounded, data-backed recommendation at a time.

Built for the **Agentic Cinema** hackathon.

## The problem

Streaming platforms generate huge volumes of viewer events, but raw
events are hard for content and streaming teams to act on. Someone still
has to manually dig through dashboards to find what matters. StudioPulse
closes that gap: it does the digging, cites the evidence, and recommends
what to do next.

## How it works

```
Raw viewer events
      |
  ClickHouse                (audience event storage)
      |
Python Analytics Engine     (aggregation queries)
      |
   FastAPI                  (REST API)
      |
 React Dashboard            (visual analytics)
      |
Gemini Agent (Google ADK)   (tool-calling audience intelligence agent)
      |
Actionable audience insight (insight + evidence + recommendation + confidence)
```

The AI layer is a genuine **agent**, not a single prompt-to-JSON call: it
is built with Google's Agent Development Kit (ADK) and is given tools
that query real ClickHouse analytics (overview, films, countries,
genres, devices, age groups, event types, country x genre). The agent
decides which data to pull before producing its insight, and is
instructed to ground every claim in numbers it actually retrieved,
avoid causal claims from observational data, and acknowledge when
differences are small.

## Live demo

- **Dashboard:** _add your deployed Vercel URL here_
- **API:** _add your deployed Render URL here_
- **Demo video:** _add your video link here_

## Tech stack

- **Database:** ClickHouse Cloud
- **Backend:** Python, FastAPI, clickhouse-connect
- **AI:** Google Gemini, Google ADK (Agent Development Kit)
- **Frontend:** React, Vite, Tailwind CSS, Recharts

## Running locally

### Backend

```bash
cd agent
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
copy ..\.env.example ..\.env    # then fill in real values
uvicorn api:app --reload
```

The API runs on `http://127.0.0.1:8000`.

### Frontend

```bash
cd dashboard
npm install
npm run dev
```

The dashboard runs on `http://localhost:5173`.

## Environment variables

See `.env.example` at the project root. The backend needs a ClickHouse
Cloud connection and a Gemini API key:

```
CLICKHOUSE_HOST=
CLICKHOUSE_USER=
CLICKHOUSE_PASSWORD=
CLICKHOUSE_SECURE=
GEMINI_API_KEY=
```

## API endpoints

| Endpoint | Description |
|---|---|
| `GET /api/overview` | High-level KPIs (events, viewers, films, completion, watch time) |
| `GET /api/films` | Per-film performance |
| `GET /api/countries` | Performance by viewer country |
| `GET /api/genres` | Performance by genre |
| `GET /api/devices` | Performance by device |
| `GET /api/age-groups` | Performance by age group |
| `GET /api/events` | Breakdown by event type |
| `GET /api/country-genres` | Country x genre performance |
| `GET /api/activity` | Viewer activity over time |
| `GET /api/ai-insights` | Agent-generated, evidence-based audience insight |

## Data note

The current dataset is observational analytics (~5,000 events, ~1,200
unique viewers, 8 films). All insights are descriptive, not causal —
the AI agent is explicitly instructed not to claim that one variable
causes another, and to flag when a difference in the data is small.

## License

MIT — see [LICENSE](./LICENSE).
MDEOF
cat /home/claude/readme_draft.md
Output

# StudioPulse

**Real-time audience intelligence for film and streaming teams.**

StudioPulse turns raw viewer-event data into evidence-based, actionable
audience insights. It ingests streaming/viewing events into ClickHouse,
computes audience analytics with a Python analytics engine, exposes them
through a FastAPI backend, visualizes them in a React dashboard, and uses
a Gemini-powered agent to interpret the analytics and surface one
grounded, data-backed recommendation at a time.

Built for the **Agentic Cinema** hackathon.

## The problem

Streaming platforms generate huge volumes of viewer events, but raw
events are hard for content and streaming teams to act on. Someone still
has to manually dig through dashboards to find what matters. StudioPulse
closes that gap: it does the digging, cites the evidence, and recommends
what to do next.

## How it works

```
Raw viewer events
      |
  ClickHouse                (audience event storage)
      |
Python Analytics Engine     (aggregation queries)
      |
   FastAPI                  (REST API)
      |
 React Dashboard            (visual analytics)
      |
Gemini Agent (Google ADK)   (tool-calling audience intelligence agent)
      |
Actionable audience insight (insight + evidence + recommendation + confidence)
```

The AI layer is a genuine **agent**, not a single prompt-to-JSON call: it
is built with Google's Agent Development Kit (ADK) and is given tools
that query real ClickHouse analytics (overview, films, countries,
genres, devices, age groups, event types, country x genre). The agent
decides which data to pull before producing its insight, and is
instructed to ground every claim in numbers it actually retrieved,
avoid causal claims from observational data, and acknowledge when
differences are small.

## Live demo

- **Dashboard:** https://studiopulse-rouge.vercel.app/
- **API:** https://studiopulse-api.onrender.com
- **Demo video:** https://youtu.be/YHGvoHTY4WY

## Tech stack

- **Database:** ClickHouse Cloud
- **Backend:** Python, FastAPI, clickhouse-connect
- **AI:** Google Gemini, Google ADK (Agent Development Kit)
- **Frontend:** React, Vite, Tailwind CSS, Recharts

## Running locally

### Backend

```bash
cd agent
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
copy ..\.env.example ..\.env    # then fill in real values
uvicorn api:app --reload
```

The API runs on `http://127.0.0.1:8000`.

### Frontend

```bash
cd dashboard
npm install
npm run dev
```

The dashboard runs on `http://localhost:5173`.

## Environment variables

See `.env.example` at the project root. The backend needs a ClickHouse
Cloud connection and a Gemini API key:

```
CLICKHOUSE_HOST=
CLICKHOUSE_USER=
CLICKHOUSE_PASSWORD=
CLICKHOUSE_SECURE=
GEMINI_API_KEY=
```

## API endpoints

| Endpoint | Description |
|---|---|
| `GET /api/overview` | High-level KPIs (events, viewers, films, completion, watch time) |
| `GET /api/films` | Per-film performance |
| `GET /api/countries` | Performance by viewer country |
| `GET /api/genres` | Performance by genre |
| `GET /api/devices` | Performance by device |
| `GET /api/age-groups` | Performance by age group |
| `GET /api/events` | Breakdown by event type |
| `GET /api/country-genres` | Country x genre performance |
| `GET /api/activity` | Viewer activity over time |
| `GET /api/ai-insights` | Agent-generated, evidence-based audience insight |

## Data note

The current dataset is observational analytics (~5,000 events, ~1,200
unique viewers, 8 films). All insights are descriptive, not causal —
the AI agent is explicitly instructed not to claim that one variable
causes another, and to flag when a difference in the data is small.

## License

MIT — see [LICENSE](./LICENSE).