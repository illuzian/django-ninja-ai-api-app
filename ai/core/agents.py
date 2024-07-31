from langchain.agents import AgentType, initialize_agent

from .providers import llm_chat


def get_agent():
    # tk.__pydantic_model__.update_forward_refs()
    # o365toolkit.account = account

    return initialize_agent(
        tools=[],
        llm=llm_chat,
        verbose=True,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
    )
