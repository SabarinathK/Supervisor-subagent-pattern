# Supervisor-subagent-pattern

A small LangChain + Groq example that uses a supervisor agent to coordinate a set of subagents for planning, coding, execution, review, and fixing.

## What this project does

The application in `src/main.py` creates a supervisor agent that:

1. asks a planner agent to break the task into steps,
2. asks a coder agent to generate Python code,
3. executes the code with an executor agent,
4. reviews the result with a reviewer agent, and
5. uses a fixer agent if the output is broken.

This is a simple pattern for building multi-agent workflows with structured tool calls.

## Project structure

- `src/main.py` — entry point for the supervisor workflow
- `src/tools.py` — tool-enabled subagents
- `src/config.py` — Groq model configuration
- `src/state.py` — structured output models for planning and review
- `src/sample_sales.csv` — sample input data used by the example task

## Prerequisites

- Python 3.12+
- uv
- A Groq API key in your environment

## Setup

1. Clone the repository
2. Create a `.env` file in the project root and add your Groq key:

   ```env
   GROQ_API_KEY=your_api_key_here
   ```

3. Install dependencies with uv:

   ```bash
   uv sync
   ```

4. Run the example:

   ```bash
   uv run python src/main.py
   ```

## Notes

- The example writes generated code to `generated_script.py` during execution.
- The current setup uses the Groq model configured in `src/config.py`.
- If you want to change the model or prompts, update the configuration in `src/config.py` and `src/tools.py`.

## License

This project is provided as-is for experimentation and learning.
