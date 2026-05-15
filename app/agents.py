#Criar agentes

from dotenv import load_dotenv
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)

joe = AssistantAgent(
    name="Joe",
    system_message=(
        "You are Joe, a stand-up comedian. "
        "Start the next joke from the punchline "
        "of the previous joke."
    ),
    model_client=model_client,
)

cathy = AssistantAgent(
    name="Cathy",
    system_message=(
        "You are Cathy, a stand-up comedian."
    ),
    model_client=model_client,
)

#Criar conversa multi-agent

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination


async def run_chat(turns=6):

    termination = MaxMessageTermination(turns)

    team = RoundRobinGroupChat(
        participants=[joe, cathy],
        termination_condition=termination,
    )

    result = await team.run(
        task="Joe, let's keep the jokes rolling."
    )

    return result