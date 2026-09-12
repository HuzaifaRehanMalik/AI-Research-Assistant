import asyncio

import streamlit as st
from agents import Runner

from core_agents.agent import research_agent
from database import initialize_database
from tools.memory import (
    create_session,
    delete_session,
    get_sessions,
    load_history,
    rename_chat,
    save_message,
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DATABASE
# =========================================================

initialize_database()


# =========================================================
# SESSION STATE
# =========================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = None


if "messages" not in st.session_state:
    st.session_state.messages = []


# =========================================================
# CHAT FUNCTIONS
# =========================================================


def load_chat(session_id):
    """Load an existing conversation."""

    history = load_history(session_id)

    st.session_state.session_id = session_id

    st.session_state.messages = history


def new_chat():
    """Create a new conversation."""

    session_id = create_session("New Chat")

    st.session_state.session_id = session_id

    st.session_state.messages = []


def generate_title(text):
    """Create a short chat title."""

    title = " ".join(text.strip().split())

    if len(title) > 45:
        title = title[:45].rstrip() + "..."

    return title or "New Chat"


async def run_agent(user_input):
    """Run the research agent."""

    session_id = st.session_state.session_id

    save_message(
        session_id,
        "user",
        user_input,
    )

    history = load_history(session_id)

    stream = Runner.run_streamed(
        research_agent,
        history,
    )

    answer = ""

    async for event in stream.stream_events():
        if event.type == "raw_response_event":
            data = getattr(
                event,
                "data",
                None,
            )

            if hasattr(data, "delta"):
                answer += data.delta

                yield {
                    "type": "text",
                    "content": data.delta,
                }

        elif event.type == "run_item_stream_event":
            item = getattr(
                event,
                "item",
                None,
            )

            if item:
                yield {
                    "type": "tool",
                    "content": item.__class__.__name__,
                }

    save_message(
        session_id,
        "assistant",
        answer,
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.title("🔬 AI Research Assistant")

    st.divider()

    if st.button(
        "➕ New Chat",
        use_container_width=True,
    ):
        new_chat()

        st.rerun()

    st.divider()

    st.subheader("💬 Chat History")

    sessions = get_sessions()

    if not sessions:
        st.caption("No previous conversations.")

    else:
        for session in sessions:
            session_id = session["id"]

            title = session["title"] or "Untitled Chat"

            is_current = session_id == st.session_state.session_id

            button_text = f"🟢 {title}" if is_current else f"💬 {title}"

            if st.button(
                button_text,
                key=f"chat_{session_id}",
                use_container_width=True,
            ):
                load_chat(session_id)

                st.rerun()

    st.divider()

    if st.session_state.session_id:
        st.subheader("Chat Options")

        new_title = st.text_input(
            "Rename chat",
            key="rename_input",
        )

        if (
            st.button(
                "Rename",
                use_container_width=True,
            )
            and new_title.strip()
        ):
            rename_chat(
                st.session_state.session_id,
                new_title.strip(),
            )

            st.rerun()

        if st.button(
            "🗑️ Delete Chat",
            use_container_width=True,
        ):
            delete_session(st.session_state.session_id)

            st.session_state.session_id = None

            st.session_state.messages = []

            st.rerun()


# =========================================================
# MAIN UI
# =========================================================

st.title("🔬 AI Research Assistant")

st.caption("Research the web, analyze webpages, and create files with AI.")


# =========================================================
# DISPLAY HISTORY
# =========================================================

for message in st.session_state.messages:
    role = message["role"]

    content = message["content"]

    if role not in (
        "user",
        "assistant",
    ):
        continue

    with st.chat_message(role):
        st.markdown(content)


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input("What would you like me to research?")


if user_input:
    # -----------------------------------------------------
    # Create session if necessary
    # -----------------------------------------------------

    if st.session_state.session_id is None:
        title = generate_title(user_input)

        st.session_state.session_id = create_session(title)

    # -----------------------------------------------------
    # Display user message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # -----------------------------------------------------
    # Assistant
    # -----------------------------------------------------

    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        status = st.status(
            "🔎 Researching...",
            expanded=True,
        )

        full_response = ""

        try:

            async def consume():

                response = ""

                async for event in run_agent(user_input):
                    if event["type"] == "text":
                        response += event["content"]

                        response_placeholder.markdown(response)

                    elif event["type"] == "tool":
                        status.write(f"🔧 Using tool: `{event['content']}`")

                return response

            full_response = asyncio.run(consume())

            status.update(
                label="✅ Research completed",
                state="complete",
                expanded=False,
            )

        except Exception as error:  # noqa: BLE001 - Streamlit boundary reports all agent failures.
            status.update(
                label="❌ Research failed",
                state="error",
                expanded=True,
            )

            st.error(str(error))

        if full_response:
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": full_response,
                }
            )
