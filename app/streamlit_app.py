import streamlit as st
import asyncio

from agents import run_chat

st.set_page_config(
    page_title="AI Agent Playground",
    layout="wide"
)

st.title(
    "AI Agent Playground — Multi-Agent Conversation"
)

st.caption(
    "Multi-agent orchestration using AutoGen + OpenAI"
)

st.markdown("""
This demo showcases autonomous interaction
between multiple AI agents using Microsoft's
AutoGen framework.
""")

st.divider()

left, right = st.columns([1, 2])

with left:

    st.subheader("Configuration")

    topic = st.text_area(
        "Conversation topic",
        value="Joe and Cathy, create a stand-up comedy routine."
    )

    # ALTERAÇÃO:
    # max turns real
    max_turns = st.slider(
        "Max turns",
        min_value=2,
        max_value=12,
        value=4,
        step=1
    )

    run_button = st.button(
        "Run Agents",
        use_container_width=True
    )

with right:

    st.subheader("Conversation")

    if run_button:

        with st.spinner("Agents thinking..."):

            try:
                result = asyncio.run(
                    run_chat(
                        topic=topic,
                        max_turns=max_turns
                    )
                )

                for msg in result.messages:

                    if getattr(
                        msg,
                        "source",
                        ""
                    ) == "user":
                        continue

                    if hasattr(msg, "source"):

                        with st.chat_message(
                            msg.source
                        ):
                            st.write(
                                msg.content
                            )

            except Exception as e:
                st.error(str(e))
                st.exception(e)

st.divider()

st.markdown("""
### What this demonstrates

- Multi-agent orchestration
- Agent-to-agent communication
- Autonomous conversations
- LLM-powered collaboration
- Production deployment
""")

st.markdown("""
### Architecture

User → Streamlit UI → AutoGen Team  
→ Joe Agent ↔ Cathy Agent  
→ OpenAI API
""")