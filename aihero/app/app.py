import asyncio
import streamlit as st
from pydantic_ai.exceptions import ModelHTTPError

import ingest
import search_agent
import logs


# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Learning Data Engineering Q&A - Powered by Groq",
    page_icon="📚",
    layout="centered",
)


# ── Agent initialisation (cached — runs once per session) ──────────────────
@st.cache_resource
def init():
    with st.spinner("📦 Loading your data engineering notes..."):
        index = ingest.index_data("Joyan9", "learning_data_engineering")
    agent = search_agent.init_agent(index)
    return agent


agent = init()


# ── UI ─────────────────────────────────────────────────────────────────────
st.title("📚 Learning Data Engineering Q&A")
st.caption("Ask anything about your data engineering study notes.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ── Streaming helper ────────────────────────────────────────────────────────
def stream_response(prompt: str):
    """
    Generator that yields text deltas from the agent stream.
    Stores the completed text and any error in st.session_state so the
    caller can access them after the generator is exhausted.
    """
    async def agen():
        async with agent.run_stream(user_prompt=prompt) as result:
            last_len = 0
            full_text = ""
            async for chunk in result.stream_output(debounce_by=0.01):
                delta = chunk[last_len:]
                last_len = len(chunk)
                full_text = chunk
                if delta:
                    yield delta
            logs.log_interaction_to_file(agent, result.new_messages())
            st.session_state._last_response = full_text

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    agen_obj = agen()

    try:
        while True:
            piece = loop.run_until_complete(agen_obj.__anext__())
            yield piece
    except StopAsyncIteration:
        return


# ── Chat input ──────────────────────────────────────────────────────────────
if prompt := st.chat_input("Ask your question..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream assistant response
    with st.chat_message("assistant"):
        try:
            response_text = st.write_stream(stream_response(prompt))
            final_text = getattr(st.session_state, "_last_response", response_text)
            st.session_state.messages.append(
                {"role": "assistant", "content": final_text}
            )

        except ModelHTTPError as e:
            if e.status_code == 429:
                msg = (
                    "⚠️ **Groq rate limit reached.** "
                    "You've used up the free-tier token quota for today. "
                    "Please wait a while and try again, or upgrade to the Groq Dev tier."
                )
            else:
                msg = f"⚠️ **Model error ({e.status_code}).** {str(e)}"
            st.warning(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})

        except Exception as e:
            msg = f"⚠️ **Unexpected error:** {str(e)}"
            st.error(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})