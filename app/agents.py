from dotenv import load_dotenv
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

joe = AssistantAgent(
    name="Joe",
    system_message="""
You are Joe, a witty stand-up comedian.

Build naturally on the previous joke.

Keep responses short:
maximum 2 sentences.
""",
    model_client=model_client,
)

cathy = AssistantAgent(
    name="Cathy",
    system_message="""
You are Cathy, a sharp stand-up comedian.

Build naturally on Joe's joke.

Keep responses short:
maximum 2 sentences.
""",
    model_client=model_client,
)


async def run_chat(
    topic: str,
    max_turns: int = 2
):
    # IMPORTANTE:
    # Cada turn = 1 mensagem de um agente
    termination = MaxMessageTermination(
        max_messages=max_turns
    )

    team = RoundRobinGroupChat(
        participants=[joe, cathy],
        termination_condition=termination,
    )

    result = await team.run(
        task=topic
    )

    return result