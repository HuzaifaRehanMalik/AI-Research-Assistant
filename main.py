import asyncio

from agents import Runner
from dotenv import load_dotenv

from core_agents.agent import research_agent
from database import initialize_database
from tools.memory import (
    create_session,
    load_history,
    save_message,
)

load_dotenv()


async def chat():

    print("=" * 60)
    print("🔍 AI Research Agent")
    print("=" * 60)
    print("Type 'exit' or 'quit' to leave.\n")

    # Create database tables
    initialize_database()

    # Start a new session
    session_id = create_session("CLI Chat")

    print(f"Session ID: {session_id}\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("\n👋 Goodbye!")
            break

        try:
            # Save user message
            save_message(
                session_id=session_id,
                role="user",
                content=user_input,
            )

            # Load previous conversation
            history = load_history(session_id)

            # -------------------------------
            # STREAMING GOES HERE
            # -------------------------------

            print("\n🤖 Agent:\n", end="", flush=True)

            stream = Runner.run_streamed(
                research_agent,
                history,
            )

            answer = ""

            async for event in stream.stream_events():
                # Stream text tokens
                if event.type == "raw_response_event":
                    data = getattr(event, "data", None)

                    if hasattr(data, "delta"):
                        print(data.delta, end="", flush=True)
                        answer += data.delta

                # Optional: display tool usage
                elif event.type == "run_item_stream_event":
                    item = getattr(event, "item", None)

                    if item:
                        print(f"\n\n🔧 Tool: {item.__class__.__name__}\n")

            print("\n")

            # Save assistant response
            save_message(
                session_id=session_id,
                role="assistant",
                content=answer,
            )

        except KeyboardInterrupt:
            print("\n\nInterrupted.")
            break

        except Exception as e:  # noqa: BLE001 - CLI boundary reports all agent failures.
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(chat())
