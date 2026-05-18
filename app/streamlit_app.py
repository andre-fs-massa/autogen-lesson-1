import streamlit as st
import asyncio

from agents import run_chat


# Page configuration
st.set_page_config(
    page_title="AI Agent Playground",
    layout="wide"
)


# Title
st.title(
    "AI Agent Playground"
)

st.caption(
    "Multi-agent conversation using AutoGen and OpenAI"
)

st.divider()


# Left / Right layout
left, right = st.columns([1, 2])


with left:

    st.subheader("Configuration")

    # Fixed topics
    topic = st.selectbox(
        "Conversation topic",
        [
            "Stand-up Comedy",
            "About AI",
            "About Engineering"
        ]
    )

    # Stop method
    stop_method = st.radio(
        "Conversation stop method",
        [
            "Max turns",
            "Termination message"
        ]
    )

    # Max turns only appears if selected
    if stop_method == "Max turns":

        max_turns = st.slider(
            "Max turns",
            min_value=2,
            max_value=6,
            value=4
        )

    else:
        max_turns = 4

        st.info(
            "Conversation ends when an agent says: 'I gotta go'"
        )

    # Run button
    run_button = st.button(
        "Run Conversation",
        use_container_width=True
    )


with right:

    st.subheader("Conversation")

    if run_button:

        with st.spinner(
            "Agents are talking..."
        ):

            try:

                result = asyncio.run(
                    run_chat(
                        topic=topic,
                        stop_method=stop_method,
                        max_turns=max_turns
                    )
                )

                # Show messages
                for msg in result.messages:

                    # Skip initial task prompt
                    if getattr(
                        msg,
                        "source",
                        ""
                    ) == "user":
                        continue

                    with st.chat_message(
                        msg.source
                    ):
                        st.write(
                            msg.content
                        )

            except Exception as e:
                st.error(str(e))


st.divider()

st.markdown("""
### What this demonstrates

- Multi-agent communication  
- Autonomous conversations  
- Conversation termination logic  
- LLM orchestration using AutoGen  
""")