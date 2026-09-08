import { useCallback, useEffect, useState } from 'react'
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts'

const API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

const tooltipStyle = {
  backgroundColor: '#1f1b29',
  border: '1px solid #2a2536',
  borderRadius: '6px',
  color: '#f1e9dc',
}

const axisTick = { fill: '#a79c8f', fontSize: 11 }
const gridStroke = '#2a2536'

const CONFIDENCE_STYLES = {
  High: 'border-gold/30 bg-gold/10 text-gold',
  Medium: 'border-teal/30 bg-teal/10 text-teal',
  Low: 'border-muted/30 bg-muted/10 text-muted',
}

function App() {
  const [overview, setOverview] = useState(null)
  const [films, setFilms] = useState([])
  const [countries, setCountries] = useState([])
  const [genres, setGenres] = useState([])
  const [devices, setDevices] = useState([])
  const [ageGroups, setAgeGroups] = useState([])
  const [events, setEvents] = useState([])
  const [activity, setActivity] = useState([])
  const [aiInsight, setAiInsight] = useState(null)
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [error, setError] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(null)

  const loadAnalytics = useCallback(async (isRefresh) => {
    if (isRefresh) setRefreshing(true)
    setError(null)

    try {
      const [
        overviewRes,
        filmsRes,
        countriesRes,
        genresRes,
        devicesRes,
        ageGroupsRes,
        eventsRes,
        activityRes,
        aiRes,
      ] = await Promise.all([
        fetch(`${API}/api/overview`),
        fetch(`${API}/api/films`),
        fetch(`${API}/api/countries`),
        fetch(`${API}/api/genres`),
        fetch(`${API}/api/devices`),
        fetch(`${API}/api/age-groups`),
        fetch(`${API}/api/events`),
        fetch(`${API}/api/activity`),
        fetch(`${API}/api/ai-insights`),
      ])

      if (
        !overviewRes.ok ||
        !filmsRes.ok ||
        !countriesRes.ok ||
        !genresRes.ok ||
        !devicesRes.ok ||
        !ageGroupsRes.ok ||
        !eventsRes.ok ||
        !activityRes.ok
      ) {
        throw new Error('Failed to load analytics data')
      }

      setOverview(await overviewRes.json())
      setFilms(await filmsRes.json())
      setCountries(await countriesRes.json())
      setGenres(await genresRes.json())
      setDevices(await devicesRes.json())
      setAgeGroups(await ageGroupsRes.json())
      setEvents(await eventsRes.json())
      setActivity(await activityRes.json())

      // AI is important, but don't break the whole dashboard
      // if Gemini is temporarily unavailable.
      if (aiRes.ok) {
        setAiInsight(await aiRes.json())
      } else {
        console.warn('AI insights unavailable')
        setAiInsight(null)
      }

      setLastUpdated(new Date())
    } catch (err) {
      console.error(err)
      setError('Unable to connect to the StudioPulse analytics API.')
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }, [])

  useEffect(() => {
    loadAnalytics(false)
  }, [loadAnalytics])

  if (loading) {
    return (
      <div className="min-h-screen bg-ink text-cream flex items-center justify-center">
        <div className="text-center">
          <div className="font-display text-4xl tracking-wide text-gold">
            StudioPulse
          </div>

          <p className="mt-3 text-muted">
            Loading analytics...
          </p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-ink text-cream flex items-center justify-center p-6">
        <div className="max-w-md rounded-md border border-cinered/30 bg-cinered/10 p-8 text-center">
          <h1 className="text-2xl font-bold text-cinered">
            Connection Error
          </h1>

          <p className="mt-3 text-cream/80">
            {error}
          </p>

          <p className="mt-4 text-sm text-muted">
            Make sure the FastAPI server is running on port 8000.
          </p>
        </div>
      </div>
    )
  }

  const deviceData = devices.map((item) => ({
    name: item.device,
    value: item.unique_viewers,
  }))

  const kpis = [
    { label: 'Total Events', value: overview.total_events.toLocaleString() },
    { label: 'Unique Viewers', value: overview.unique_viewers.toLocaleString() },
    { label: 'Films', value: overview.films },
    { label: 'Avg Completion', value: `${overview.avg_completion_percent}%` },
    { label: 'Avg Watch Time', value: `${(overview.avg_watch_seconds / 60).toFixed(1)}m` },
  ]

  return (
    <div className="min-h-screen bg-ink text-cream">

      {/* Header */}
      <header className="border-b border-panel-light bg-ink/95">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-6 py-5">
          <div>
            <h1 className="font-display text-4xl tracking-wide">
              Studio<span className="text-gold">Pulse</span>
            </h1>

            <p className="text-sm text-muted">
              Real-time audience intelligence for streaming
            </p>
          </div>

          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-400"></span>
              <span className="text-sm text-muted">Live</span>
            </div>

            {lastUpdated && (
              <span className="text-xs text-muted">
                Updated {lastUpdated.toLocaleTimeString()}
              </span>
            )}

            <button
              onClick={() => loadAnalytics(true)}
              disabled={refreshing}
              className="rounded-md border border-panel-light bg-panel px-3 py-1.5 text-sm text-cream transition hover:border-gold/40 hover:text-gold disabled:opacity-50"
            >
              {refreshing ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-8">

        {/* Page heading */}
        <div className="mb-8">
          <h2 className="font-display text-3xl tracking-wide">
            Analytics Overview
          </h2>

          <p className="mt-2 text-muted">
            Understand how viewers interact with your content.
          </p>
        </div>

        {/* KPI ticker */}
        <div className="flex divide-x divide-panel-light overflow-x-auto rounded-md border border-panel-light bg-panel">
          {kpis.map((kpi) => (
            <div key={kpi.label} className="min-w-[140px] flex-1 px-5 py-4">
              <p className="text-xs text-muted">{kpi.label}</p>
              <p className="mt-1 text-2xl font-bold tabular-nums text-cream">
                {kpi.value}
              </p>
            </div>
          ))}
        </div>

        {/* Viewer Activity */}
        <div className="mt-8">
          <ChartCard
            title="Viewer Activity"
            description="Events and unique viewers over time"
          >
            <ResponsiveContainer width="100%" height={320}>
              <LineChart data={activity}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />

                <XAxis
                  dataKey="hour"
                  tick={axisTick}
                  tickFormatter={(value) =>
                    new Date(value).toLocaleDateString([], {
                      month: 'short',
                      day: 'numeric',
                    })
                  }
                />

                <YAxis tick={axisTick} />

                <Tooltip
                  contentStyle={tooltipStyle}
                  labelFormatter={(value) => new Date(value).toLocaleString()}
                />

                <Line
                  type="monotone"
                  dataKey="events"
                  stroke="#d9a441"
                  strokeWidth={2}
                  dot={false}
                  name="Events"
                />

                <Line
                  type="monotone"
                  dataKey="unique_viewers"
                  stroke="#3e7c82"
                  strokeWidth={2}
                  dot={false}
                  name="Unique Viewers"
                />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* AI Insights */}
        <div className="mt-6">
          <section className="rounded-md border-t-2 border-cinered bg-panel p-6">

            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <h3 className="font-display text-2xl tracking-wide">
                  AI Insights
                </h3>

                <p className="mt-1 text-sm text-muted">
                  Audience intelligence generated from your analytics
                </p>
              </div>

              {aiInsight && (
                <span
                  className={`rounded-full border px-3 py-1 text-xs font-medium ${
                    CONFIDENCE_STYLES[aiInsight.confidence] || CONFIDENCE_STYLES.Low
                  }`}
                >
                  Confidence: {aiInsight.confidence}
                </span>
              )}
            </div>

            {aiInsight ? (
              <div className="mt-6 grid gap-5 lg:grid-cols-3">
                <InsightBlock title="Insight" text={aiInsight.insight} />
                <InsightBlock title="Evidence" text={aiInsight.evidence} />
                <InsightBlock
                  title="Recommendation"
                  text={aiInsight.recommendation}
                />
              </div>
            ) : (
              <div className="mt-5 rounded-md border border-panel-light bg-ink/50 p-5">
                <p className="text-sm text-muted">
                  AI insights are temporarily unavailable. Your analytics
                  dashboard is still fully operational.
                </p>
              </div>
            )}

          </section>
        </div>

        {/* Main charts */}
        <div className="mt-8 grid gap-6 lg:grid-cols-2">

          {/* Films */}
          <ChartCard
            title="Film Performance"
            description="Average completion rate by film"
          >
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={films}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />

                <XAxis
                  dataKey="film_title"
                  tick={{ ...axisTick }}
                  angle={-20}
                  textAnchor="end"
                  height={70}
                />

                <YAxis domain={[0, 100]} tick={axisTick} />

                <Tooltip contentStyle={tooltipStyle} />

                <Bar
                  dataKey="avg_completion_percent"
                  fill="#d9a441"
                  radius={[5, 5, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>

          {/* Countries */}
          <ChartCard
            title="Country Performance"
            description="Audience completion by country"
          >
            <ResponsiveContainer width="100%" height={320}>
              <BarChart data={countries}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />

                <XAxis dataKey="country" tick={axisTick} />

                <YAxis domain={[0, 100]} tick={axisTick} />

                <Tooltip contentStyle={tooltipStyle} />

                <Bar
                  dataKey="avg_completion_percent"
                  fill="#3e7c82"
                  radius={[5, 5, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>

        </div>

        {/* Secondary charts */}
        <div className="mt-6 grid gap-6 lg:grid-cols-3">

          {/* Genres */}
          <ChartCard
            title="Genre Performance"
            description="Completion rate by genre"
          >
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={genres}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />

                <XAxis
                  dataKey="genre"
                  tick={{ ...axisTick }}
                  angle={-20}
                  textAnchor="end"
                  height={60}
                />

                <YAxis domain={[0, 100]} tick={axisTick} />

                <Tooltip contentStyle={tooltipStyle} />

                <Bar
                  dataKey="avg_completion_percent"
                  fill="#b23a48"
                  radius={[5, 5, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>

          {/* Devices */}
          <ChartCard
            title="Device Distribution"
            description="Unique viewers by device"
          >
            <ResponsiveContainer width="100%" height={280}>
              <PieChart>
                <Pie
                  data={deviceData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={90}
                  label
                >
                  {deviceData.map((_, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={['#d9a441', '#3e7c82', '#b23a48', '#8b6f47'][index % 4]}
                    />
                  ))}
                </Pie>

                <Tooltip contentStyle={tooltipStyle} />
              </PieChart>
            </ResponsiveContainer>
          </ChartCard>

          {/* Age groups */}
          <ChartCard
            title="Age Groups"
            description="Viewer distribution by age"
          >
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={ageGroups}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />

                <XAxis dataKey="age_group" tick={axisTick} />

                <YAxis tick={axisTick} />

                <Tooltip contentStyle={tooltipStyle} />

                <Bar
                  dataKey="unique_viewers"
                  fill="#d9a441"
                  radius={[5, 5, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>

        </div>

        {/* Event breakdown */}
        <div className="mt-6">
          <ChartCard
            title="Event Activity"
            description="Viewer interaction events"
          >
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={events}>
                <CartesianGrid strokeDasharray="3 3" stroke={gridStroke} />

                <XAxis dataKey="event_type" tick={axisTick} />

                <YAxis tick={axisTick} />

                <Tooltip contentStyle={tooltipStyle} />

                <Bar
                  dataKey="events"
                  fill="#3e7c82"
                  radius={[5, 5, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

      </main>

      <footer className="border-t border-panel-light py-6 text-center text-sm text-muted">
        StudioPulse Analytics — Powered by ClickHouse, FastAPI, and Gemini
      </footer>

    </div>
  )
}

function ChartCard({ title, description, children }) {
  return (
    <section className="rounded-md border-t-2 border-panel-light bg-panel p-5">
      <div className="mb-5">
        <h3 className="text-lg font-semibold text-cream">{title}</h3>
        <p className="mt-1 text-sm text-muted">{description}</p>
      </div>

      {children}
    </section>
  )
}

function InsightBlock({ title, text }) {
  return (
    <div className="rounded-md border border-panel-light bg-ink/40 p-5">
      <p className="text-sm font-semibold text-gold">{title}</p>
      <p className="mt-3 text-sm leading-6 text-cream/90">{text}</p>
    </div>
  )
}

export default App
