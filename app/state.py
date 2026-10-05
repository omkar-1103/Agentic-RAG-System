from typing import TypedDict, Annotated, List, Dict, Any
import operator

def merge_list(a: list, b: list) -> list:
    return a + b

class GraphState(TypedDict):
    """
    Represents the state of our graph.
    """
    original_query: str
    intent: str
    complexity: str
    requires_tools: bool
    is_in_domain: bool
    plan: list[dict] # Contains tool assignments
    
    # We use Annotated with operator.add to append evidence rather than overwriting
    raw_evidence: Annotated[list[dict], merge_list]
    
    fused_evidence: str
    draft_answer: str
    checker_feedback: str
    is_valid: bool
    retry_count: int
