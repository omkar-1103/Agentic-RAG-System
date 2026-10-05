from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from app.utils.logger import logger
from app.state import GraphState
from app.prompts import REASONER_PROMPT

llm = ChatOllama(model="qwen2.5", temperature=0)

def reasoner_node(state: GraphState) -> dict:
    """Synthesizes the fused evidence to answer the original query."""
    logger.info("---REASONING---")
    query = state["original_query"]
    evidence = state.get("fused_evidence", "")
    
    messages = [
        SystemMessage(content=REASONER_PROMPT),
        HumanMessage(content=f"Query: {query}\n\n{evidence}")
    ]
    
    response = llm.invoke(messages)
    
    content = response.content
    if isinstance(content, list):
        # Extract text from the new structured Gemini output format
        extracted_text = ""
        for item in content:
            if isinstance(item, dict) and "text" in item:
                extracted_text += item["text"]
            elif isinstance(item, str):
                extracted_text += item
        content = extracted_text
    
    return {"draft_answer": content}
