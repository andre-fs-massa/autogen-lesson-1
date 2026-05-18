from dotenv import load_dotenv
import os

from autogen import ConversableAgent


# Load environment variables
load_dotenv()


# OpenAI configuration
llm_config = {
    "model": "gpt-4o-mini",
    "api_key": os.getenv("OPENAI_API_KEY")
}


def create_agents(stop_method):

    # =====================================
    # STOP METHOD:
    # TERMINATION MESSAGE
    # =====================================
    if stop_method == "Termination message":

        joe = ConversableAgent(
            name="Joe",

            system_message=(
                "Your name is Joe. "
                "You enjoy discussing topics with Cathy. "
                "When you're ready to end the conversation, "
                "say 'I gotta go'."
                "Keep the conversation short."
            ),

            llm_config=llm_config,

            human_input_mode="NEVER",

            is_termination_msg=lambda msg:
                "I gotta go" in msg["content"],
        )

        cathy = ConversableAgent(
            name="Cathy",

            system_message=(
                "Your name is Cathy. "
                "You enjoy discussing topics with Joe. "
                "When you're ready to end the conversation, "
                "say 'I gotta go'."
                "Keep the conversation short."
            ),

            llm_config=llm_config,

            human_input_mode="NEVER",

            is_termination_msg=lambda msg:
                "I gotta go" in msg["content"],
        )

    # =====================================
    # STOP METHOD:
    # MAX TURNS
    # =====================================
    else:

        joe = ConversableAgent(
            name="Joe",

            system_message=(
                "Your name is Joe. "
                "You enjoy discussing topics with Cathy."
            ),

            llm_config=llm_config,

            human_input_mode="NEVER",
        )

        cathy = ConversableAgent(
            name="Cathy",

            system_message=(
                "Your name is Cathy. "
                "You enjoy discussing topics with Joe."
            ),

            llm_config=llm_config,

            human_input_mode="NEVER",
        )

    return joe, cathy


def run_chat(
    topic,
    stop_method,
    max_turns
):

    # Create agents
    joe, cathy = create_agents(
        stop_method
    )

    # =====================================
    # TERMINATION MESSAGE MODE
    # =====================================
    if stop_method == "Termination message":

        chat_result = joe.initiate_chat(
            recipient=cathy,
            message="I'm Joe. Cathy, let's talk about this: " + topic,
        )

    # =====================================
    # MAX TURNS MODE
    # =====================================
    else:

        chat_result = joe.initiate_chat(
            recipient=cathy,
            message="I'm Joe. Cathy, let's talk about this: " + topic,
            max_turns=max_turns
        )

    return chat_result