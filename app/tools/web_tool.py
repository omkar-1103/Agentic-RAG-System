import os
from tavily import TavilyClient
from app.utils.logger import logger

def execute_web_search(query: str) -> dict:
    """
    Real implementation of a web search using Tavily API.
    """
    logger.info(f"[Web Tool] Searching web for: {query}")
    
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return {
            "source": "web_tool",
            "query": query,
            "error": "TAVILY_API_KEY is missing from .env file."
        }
        
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query=query)
        
        return {
            "source": "web_tool",
            "query": query,
            "results": response.get("results", [])
        }
    except Exception as e:
        logger.error(f"[Web Tool] Error searching Tavily: {e}")
        return {
            "source": "web_tool",
            "query": query,
            "error": str(e)
        }
