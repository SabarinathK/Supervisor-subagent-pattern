import subprocess
from langchain.tools import tool
from config import llm, planner_llm, reviewer_llm

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
