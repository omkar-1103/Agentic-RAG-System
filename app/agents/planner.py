from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from app.utils.logger import logger
from app.state import GraphState
from app.prompts import PLANNER_PROMPT
from app.schemas import PlannerOutput

llm = ChatOllama(model="qwen2.5", temperature=0)
planner_llm = llm.with_structured_output(PlannerOutput)

def planner_node(state: GraphState) -> dict:
    """Decomposes query and assigns tools."""
    logger.info("---PLANNING EXECUTION---")
    query = state["original_query"]
    intent = state.get("intent", "Unknown")
    feedback = state.get("checker_feedback", "")
    
    # If there is feedback, append it so the planner knows what went wrong
    human_msg = f"Query: {query}\nIntent: {intent}"
    if feedback:
        human_msg += f"\n\nPrevious attempt was REJECTED. Feedback: {feedback}\nPlease adjust the plan accordingly."
        
    messages = [
        SystemMessage(content=PLANNER_PROMPT),
        HumanMessage(content=human_msg)
    ]
    
    result = planner_llm.invoke(messages)
    
    # We return the plan, and also clear raw_evidence and feedback for the retry
    return {
        "plan": [step.model_dump() for step in result.plan],
        "raw_evidence": [],
        "checker_feedback": ""
    }
