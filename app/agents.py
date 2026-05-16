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

You should continue the conversation
creatively and build upon previous jokes.

Keep responses concise and funny.
""",
    model_client=model_client,
)

cathy = AssistantAgent(
    name="Cathy",
    system_message="""
You are Cathy, a sharp stand-up comedian.

You improvise based on Joe's jokes
while keeping the conversation engaging.

Keep responses concise and funny.
""",
    model_client=model_client,
)


async def run_chat(
    topic: str,
    turns: int = 4
):
    # ALTERAÇÃO:
    # cada interação = Joe + Cathy
    termination = MaxMessageTermination(
        max_messages=turns * 2
    )

    team = RoundRobinGroupChat(
        participants=[joe, cathy],
        termination_condition=termination,
    )

    # ALTERAÇÃO:
    # prompt dinâmico
    result = await team.run(
        task=topic
    )

    return result