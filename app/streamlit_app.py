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

    turns = st.slider(
        "Conversation rounds",
        min_value=2,
        max_value=6,
        value=3
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
                        turns=turns
                    )
                )

                for msg in result.messages:

                    # ALTERAÇÃO:
                    # não mostrar prompt inicial
                    if getattr(msg, "source", "") == "user":
                        continue

                    if hasattr(msg, "source"):

                        with st.chat_message(
                            msg.source
                        ):
                            st.write(
                                msg.content
                            )

            except Exception as e:
                st.error("Full error:")
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