from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from app.utils.logger import logger
from app.state import GraphState

llm = ChatOllama(model="qwen2.5", temperature=0)

def direct_responder_node(state: GraphState) -> dict:
    """Answers simple queries and greetings directly without using expensive tools."""
    logger.info("---DIRECT RESPONDER---")
    query = state["original_query"]
    
    messages = [
        SystemMessage(content="You are a helpful AI assistant. Answer the user's query directly and concisely. Do not search for external information."),
        HumanMessage(content=query)
    ]
    
    response = llm.invoke(messages)
    
    return {
        "draft_answer": response.content,
        "is_valid": True # We mark it valid so it skips the checker and finishes instantly
    }
