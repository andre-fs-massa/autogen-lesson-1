from dotenv import load_dotenv
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import (
    MaxMessageTermination,
    TextMentionTermination
)

# Load environment variables (.env)
load_dotenv()


# OpenAI model configuration
model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)


def create_agents(stop_method):

    # System prompt for termination message mode
    if stop_method == "Termination message":

        joe_prompt = """
You are Joe.

You enjoy discussing topics with Cathy.

When you want to end the conversation,
say exactly:

I gotta go

Keep responses short.
Maximum 2 sentences.
"""

        cathy_prompt = """
You are Cathy.

You enjoy discussing topics with Joe.

When you want to end the conversation,
say exactly:

I gotta go

Keep responses short.
Maximum 2 sentences.
"""

    # System prompt for max turns mode
    else:

        joe_prompt = """
You are Joe.

You enjoy discussing topics with Cathy.

Keep responses short.
Maximum 2 sentences.
"""

        cathy_prompt = """
You are Cathy.

You enjoy discussing topics with Joe.

Keep responses short.
Maximum 2 sentences.
"""

    # Create Joe agent
    joe = AssistantAgent(
        name="Joe",
        system_message=joe_prompt,
        model_client=model_client,
    )

    # Create Cathy agent
    cathy = AssistantAgent(
        name="Cathy",
        system_message=cathy_prompt,
        model_client=model_client,
    )

    return joe, cathy


async def run_chat(
    topic,
    stop_method,
    max_turns
):

    # Create agents
    joe, cathy = create_agents(
        stop_method
    )

    # Stop method 1: Max turns
    if stop_method == "Max turns":

        termination = MaxMessageTermination(
            max_messages=max_turns
        )

    # Stop method 2: Termination message
    else:

        termination = TextMentionTermination(
            "I gotta go"
        )

    # Create team
    team = RoundRobinGroupChat(
        participants=[joe, cathy],
        termination_condition=termination,
    )

    # Start conversation
    result = await team.run(
        task=topic
    )

    return result