from app.utils.logger import logger
from app.state import GraphState

def guardrail_node(state: GraphState) -> dict:
    """Politely rejects queries that fall outside the business domain."""
    logger.info("---GUARDRAIL: REJECTING OFF-TOPIC QUERY---")
    
    intent = state.get("intent", "this topic")
    
    response = f"I am a specialized corporate AI assistant. I am not equipped to help with '{intent}'. Please ask me questions related to our business, data, or analytics."
    
    return {
        "draft_answer": response,
        "is_valid": True # Skip checker
    }
