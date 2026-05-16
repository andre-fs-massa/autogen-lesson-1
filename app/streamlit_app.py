#Criar interface pública
import streamlit as st
import asyncio

from agents import run_chat

st.set_page_config(
    page_title="AutoGen Lesson 1",
    layout="wide"
)

st.title("🎭 Multi-Agent Stand-Up Comedy")

st.write(
    "Multi-Agent Conversation "
    "using AutoGen"
)

turns = st.slider(
    "Number of interactions",
    min_value=2,
    max_value=6,
    value=4
)

if st.button("Run Agents"):

    with st.spinner("Agents talking..."):

        try:
            result = asyncio.run(run_chat(turns))

            st.subheader("Conversation")

            for msg in result.messages:

                if hasattr(msg, "source"):
                    st.markdown(
                        f"**{msg.source}**: "
                        f"{msg.content}"
                    )

        except Exception as e:
            st.error("Full error:")
            st.exception(e)

    for msg in result.messages:

        if hasattr(msg, "source"):
            st.markdown(
                f"**{msg.source}**: {msg.content}"
            )