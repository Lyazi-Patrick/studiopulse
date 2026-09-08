import asyncio
import json
import uuid

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.genai.errors import ServerError

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


class AIInsightError(Exception):
    """Raised when the AI agent fails to produce a usable insight."""


async def get_ai_insight() -> dict:
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
