from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from app.utils.logger import logger
from app.state import GraphState
from app.prompts import ANALYZER_PROMPT
from app.schemas import AnalysisOutput

# Initialize LLM
llm = ChatOllama(model="qwen2.5", temperature=0)
# Bind the structured output schema
analyzer_llm = llm.with_structured_output(AnalysisOutput)

def analyzer_node(state: GraphState) -> dict:
    """Analyzes the query for intent and complexity."""
    logger.info("---ANALYZING QUERY---")
    query = state["original_query"]
    
    messages = [
        SystemMessage(content=ANALYZER_PROMPT),
        HumanMessage(content=f"Query: {query}")
    ]
    
    result = analyzer_llm.invoke(messages)
    
    return {
        "intent": result.intent,
        "complexity": result.complexity,
        "requires_tools": getattr(result, "requires_tools", True),
        "is_in_domain": getattr(result, "is_in_domain", True)
    }
