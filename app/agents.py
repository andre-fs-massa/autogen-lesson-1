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

joe = AssistantAgent(
    name="Joe",
    system_message="""
You are Joe and you are a stand-up comedian.

When you're ready to end the conversation,
say exactly: I gotta go

Keep responses short.
Maximum 2 sentences.
""",
    model_client=model_client,
)

cathy = AssistantAgent(
    name="Cathy",
    system_message="""
You are Cathy and you are a stand-up comedian.

When you're ready to end the conversation,
say exactly: I gotta go

Keep responses short.
Maximum 2 sentences.
""",
    model_client=model_client,
)


async def run_chat(
    topic: str,
    stop_method: str,
    max_turns: int = 2
):

    # ===================================
    # STOP METHOD 1
    # Igual ao curso: max_turns
    # ===================================
    if stop_method == "Max turns":

        termination = MaxMessageTermination(
            # reproduz o comportamento do curso
            max_messages=max_turns + 1
        )

    # ===================================
    # STOP METHOD 2
    # Igual ao curso:
    # is_termination_msg
    # ===================================
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