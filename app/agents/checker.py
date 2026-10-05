from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from app.utils.logger import logger
from app.state import GraphState
from app.prompts import CHECKER_PROMPT
from app.schemas import CheckerOutput

llm = ChatOllama(model="qwen2.5", temperature=0)
checker_llm = llm.with_structured_output(CheckerOutput)

def checker_node(state: GraphState) -> dict:
    """Evaluates the draft answer against the query and evidence."""
    logger.info("---CHECKING ANSWER---")
    query = state["original_query"]
    evidence = state.get("fused_evidence", "")
    answer = state.get("draft_answer", "")
    retry_count = state.get("retry_count", 0)
    
    messages = [
        SystemMessage(content=CHECKER_PROMPT),
        HumanMessage(content=f"Original Query: {query}\n\nEvidence:\n{evidence}\n\nDraft Answer:\n{answer}")
    ]
    
    result = checker_llm.invoke(messages)
    
    feedback_str = ""
    if not result.is_valid:
        feedback_str = f"Tool Selection Correct: {result.tool_selection_correct}\n"
        feedback_str += f"Missing Information: {', '.join(result.missing_information)}\n"
        feedback_str += f"Recommended Action: {result.recommended_action}"

    return {
        "is_valid": result.is_valid,
        "checker_feedback": feedback_str,
        "retry_count": retry_count + 1
    }
