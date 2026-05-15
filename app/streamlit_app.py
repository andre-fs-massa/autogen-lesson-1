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
    "Lesson 1 — Multi-Agent Conversation "
    "using AutoGen"
)

turns = st.slider(
    "Number of interactions",
    min_value=2,
    max_value=12,
    value=6
)

if st.button("Run Agents"):

    with st.spinner("Agents talking..."):

        result = asyncio.run(run_chat(turns))

    st.subheader("Conversation")

    for msg in result.messages:

        if hasattr(msg, "source"):
            st.markdown(
                f"**{msg.source}**: {msg.content}"
            )