from langchain_groq import ChatGroq
from state import PlanOutput, ReviewOutput

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

planner_llm = llm.with_structured_output(PlanOutput)
reviewer_llm = llm.with_structured_output(ReviewOutput)
