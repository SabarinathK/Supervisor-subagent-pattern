import subprocess
from typing import List

from dotenv import load_dotenv
from pydantic import BaseModel

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.agents import create_agent
from pprint import pprint

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)


class PlanOutput(BaseModel):
    tasks: List[str]


class ReviewOutput(BaseModel):
    success: bool
    feedback: str


planner_llm = llm.with_structured_output(PlanOutput)
reviewer_llm = llm.with_structured_output(ReviewOutput)


@tool
def planner_agent(user_task: str) -> str:
    """
    Break user request into executable steps.
    """
    messages = [
        (
            "system",
            "Break the user request into executable coding steps. Return short task list.",
        ),
        ("human", f"USER TASK:\n{user_task}"),
    ]
    result = planner_llm.invoke(messages)
    return "\n".join(result.tasks)


@tool
def coder_agent(task_input: str) -> str:
    """
    Generate executable python code.
    """
    messages = [
        (
            "system",
            "Generate executable python code.\n\nRULES:\n- Return ONLY python code\n- No markdown\n- No explanation",
        ),
        ("human", f"TASK:\n{task_input}"),
    ]
    response = llm.invoke(messages)
    code = response.content.strip()
    code = code.replace("```python", "").replace("```", "")
    return code


@tool
def executor_agent(code: str) -> str:
    """
    Execute generated python code.
    """
    with open("generated_script.py", "w", encoding="utf-8") as f:
        f.write(code)

    try:
        result = subprocess.run(
            ["python", "generated_script.py"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return str(e)


@tool
def reviewer_agent(review_input: str) -> str:
    """
    Review execution output.
    """
    messages = [
        (
            "system",
            "Review execution result. Decide:\n- Was task completed correctly?\n- Any runtime errors?\n- Any syntax issues?\nReturn structured output.",
        ),
        ("human", f"INPUT:\n{review_input}"),
    ]
    result = reviewer_llm.invoke(messages)
    return f"SUCCESS: {result.success}\n\nFEEDBACK:\n{result.feedback}"


@tool
def fixer_agent(fix_input: str) -> str:
    """
    Fix broken python code.
    """
    messages = [
        (
            "system",
            "Fix this python code.\n\nRULES:\n- Return ONLY fixed python code\n- No markdown\n- No explanation",
        ),
        ("human", f"INPUT:\n{fix_input}"),
    ]
    response = llm.invoke(messages)
    fixed_code = response.content.strip()
    fixed_code = fixed_code.replace("```python", "").replace("```", "")
    return fixed_code


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
