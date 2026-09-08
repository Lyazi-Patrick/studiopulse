import asyncio
import json
import time
import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.genai.errors import ServerError, ClientError

from agent import root_agent

APP_NAME = "studiopulse"
USER_ID = "studiopulse_dashboard"

_session_service = InMemorySessionService()
_runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=_session_service,
)

_PROMPT = "Find one meaningful audience insight from the StudioPulse data."
_MAX_ATTEMPTS = 3
_RETRY_DELAY_SECONDS = 2
_CACHE_TTL_SECONDS = 300  # 5 minutes


class AIInsightError(Exception):
    """Raised when the AI agent fails to produce a usable insight and no
    cached insight is available to fall back on."""


_cache = {"insight": None, "generated_at": 0.0}


async def get_ai_insight() -> dict:
    now = time.monotonic()
    cache_age = now - _cache["generated_at"]

    if _cache["insight"] is not None and cache_age < _CACHE_TTL_SECONDS:
        return _cache["insight"]

    try:
        insight = await _generate_insight()
        _cache["insight"] = insight
        _cache["generated_at"] = now
        return insight
    except AIInsightError:
        # Generation failed. If we have a previous insight (even if
        # stale), keep serving it rather than breaking the dashboard.
        if _cache["insight"] is not None:
            return _cache["insight"]
        raise


async def _generate_insight() -> dict:
    session_id = str(uuid.uuid4())
    await _session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )

    message = types.Content(
        role="user",
        parts=[types.Part(text=_PROMPT)],
    )

    last_error = None

    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            final_text = None
            async for event in _runner.run_async(
                user_id=USER_ID, session_id=session_id, new_message=message
            ):
                if event.is_final_response() and event.content and event.content.parts:
                    final_text = event.content.parts[0].text

            if not final_text:
                raise AIInsightError("Agent returned no response.")

            return json.loads(final_text)

        except ClientError as e:
            if getattr(e, "code", None) == 429:
                raise AIInsightError(
                    "Gemini's free-tier daily quota has been reached. "
                    "Please try again later or upgrade the API plan."
                ) from e
            raise AIInsightError(f"Gemini request failed: {e}") from e

        except ServerError as e:
            last_error = e
            if attempt < _MAX_ATTEMPTS:
                await asyncio.sleep(_RETRY_DELAY_SECONDS)
                continue
            raise AIInsightError(
                "Gemini is temporarily unavailable (high demand). Please try again shortly."
            ) from e

        except json.JSONDecodeError as e:
            raise AIInsightError(
                "The agent returned a response that was not valid JSON."
            ) from e

    raise AIInsightError("Unknown failure generating AI insight.") from last_error
