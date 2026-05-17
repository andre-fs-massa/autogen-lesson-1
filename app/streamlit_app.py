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
This demo reproduces Lesson 1 from
AI Agentic Design Patterns with AutoGen.
""")

st.divider()

left, right = st.columns([1, 2])

with left:

    st.subheader("Configuration")

    topic = st.text_area(
        "Conversation topic",
        value=(
            "Joe and Cathy, "
            "create a stand-up comedy routine."
        )
    )

    # ==========================
    # STOP METHOD
    # ==========================
    stop_method = st.radio(
        "Conversation stop method",
        [
            "Max turns",
            "Termination message"
        ]
    )

    # ==========================
    # MAX TURNS
    # ==========================
    if stop_method == "Max turns":

        max_turns = st.slider(
            "Max turns",
            min_value=1,
            max_value=10,
            value=2,
            help="""
Matches the course behavior.

1 = Joe + Cathy

2 = Joe + Cathy + Joe

3 = Joe + Cathy + Joe + Cathy
"""
        )

    else:
        max_turns = None

        st.info("""
Conversation ends when one agent says:

'I gotta go'
""")

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
                        stop_method=stop_method,
                        max_turns=max_turns
                    )
                )

                for msg in result.messages:

                    # remove prompt inicial
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
- Termination conditions
- Autonomous conversations
- LLM-powered collaboration
""")