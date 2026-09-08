import asyncio
import json

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent

APP_NAME = "studiopulse_test"
USER_ID = "test_user"
SESSION_ID = "test_session"


async def main():
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    runner = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    message = types.Content(
        role="user",
        parts=[types.Part(
            text="Find one meaningful audience insight from the StudioPulse data."
        )],
    )

    final_text = None
    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=message
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = event.content.parts[0].text

    print("\nRaw agent output:\n")
    print(final_text)

    print("\nParsed JSON:\n")
    print(json.dumps(json.loads(final_text), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
