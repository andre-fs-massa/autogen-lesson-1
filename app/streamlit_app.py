import streamlit as st

from agents import run_chat


# Page configuration
st.set_page_config(
    page_title="AI Agent Playground",
    layout="wide"
)


# Header
st.title(
    "AI Agent Playground"
)

st.caption(
    "Conversation between 2 agents (Joe and Cathy), using AutoGen and OpenAI"
)

st.divider()


# Layout
left, right = st.columns([1, 2])


# =====================================
# LEFT SIDE
# =====================================
with left:

    st.subheader("Configuration")

    # Fixed topics
    topic = st.selectbox(
        "Conversation topic",
        [
            "Stand-up Comedy",
            "Artificial Intelligence",
            "Engineering"
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

    # Max turns UI
    if stop_method == "Max turns":

        max_turns = st.slider(
            "Max turns",
            min_value=2,
            max_value=6,
            value=4
        )

    else:

        max_turns = None

        st.info(
            "Conversation ends when an agent says: "
            "'I gotta go'"
        )

    # Run button
    run_button = st.button(
        "Run Conversation",
        use_container_width=True
    )


# =====================================
# RIGHT SIDE
# =====================================
with right:

    st.subheader("Conversation")

    if run_button:

        with st.spinner(
            "Agents are thinking..."
        ):

            try:

                result = run_chat(
                    topic=topic,
                    stop_method=stop_method,
                    max_turns=max_turns
                )

                # Show messages
                for msg in result.chat_history:

                    role = msg.get("name")

                    # Skip system/user messages
                    if role is None:
                        continue

                    with st.chat_message(
                        role
                    ):
                        st.write(
                            msg["content"]
                        )

            except Exception as e:
                st.error(str(e))


# =====================================
# FOOTER
# =====================================
st.divider()

st.markdown("""
### What this demonstrates

- Multi-agent communication  
- Autonomous conversations  
- Conversation termination logic  
- LLM orchestration using AutoGen  
""")