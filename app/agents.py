from dotenv import load_dotenv
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import (
    MaxMessageTermination,
    TextMentionTermination
)

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)


def create_agents(stop_method: str):

    # ====================================
    # CURSO: TERMINATION MESSAGE
    # ====================================
    if stop_method == "Termination message":

        joe_system = """
You are Joe and you are a stand-up comedian.

When you're ready to end the conversation,
say exactly:

I gotta go

Keep responses short.
Maximum 2 sentences.
"""

        cathy_system = """
You are Cathy and you are a stand-up comedian.

When you're ready to end the conversation,
say exactly:

I gotta go

Keep responses short.
Maximum 2 sentences.
"""

    # ====================================
    # CURSO: MAX TURNS
    # ====================================
    else:

        joe_system = """
You are Joe and you are a stand-up comedian.

Keep the jokes rolling.

Keep responses short.
Maximum 2 sentences.
"""

        cathy_system = """
You are Cathy and you are a stand-up comedian.

Keep the jokes rolling.

Keep responses short.
Maximum 2 sentences.
"""

    joe = AssistantAgent(
        name="Joe",
        system_message=joe_system,
        model_client=model_client,
    )

    cathy = AssistantAgent(
        name="Cathy",
        system_message=cathy_system,
        model_client=model_client,
    )

    return joe, cathy


async def run_chat(
    topic: str,
    stop_method: str,
    max_turns: int = 2
):

    joe, cathy = create_agents(
        stop_method
    )

    # ====================================
    # OPÇÃO 1
    # IGUAL AO CURSO
    # ====================================
    if stop_method == "Max turns":

        termination = MaxMessageTermination(
            # replica max_turns do notebook
            max_messages=max_turns + 1
        )

    # ====================================
    # OPÇÃO 2
    # IGUAL AO CURSO
    # ====================================
    else:

        termination = TextMentionTermination(
            "I gotta go"
        )

    team = RoundRobinGroupChat(
        participants=[joe, cathy],
        termination_condition=termination,
    )

    result = await team.run(
        task=topic
    )

    return result