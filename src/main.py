from dotenv import load_dotenv

from langchain_core.tools import tool
from langchain.agents import create_agent
from pprint import pprint
from tools import (
    planner_agent,
    coder_agent,
    executor_agent,
    reviewer_agent,
    fixer_agent,
)
from config import llm

load_dotenv()

tools = [
    planner_agent,
    coder_agent,
    executor_agent,
    reviewer_agent,
    fixer_agent,
]

supervisor_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="""Use planner_agent first to map out the strategy.
    Then invoke coder_agent to build the target python code.
    Execute the code via executor_agent.
    Review the output metrics and logs with reviewer_agent.
    If bugs or dynamic validation failures occur, send inputs to fixer_agent.""",
)

if __name__ == "__main__":

    task = """
    Create a python script that:
    1. get the data from this csv "sample_sales.csv"
    2. find which product has the highest price
    3. find which city has that product
    """

    result = supervisor_agent.invoke({"messages": [("user", task)]})

    pprint(result["messages"])
