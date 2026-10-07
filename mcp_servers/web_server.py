import os
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

# Create the MCP Server
mcp = FastMCP("Tavily Web Search Server")


@mcp.tool()
def web_search(query: str) -> str:
    """Search the live internet for real-time information using Tavily.
    Returns the top 5 search results with titles and content snippets.
    """
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = client.search(query=query)
    results = response.get("results", [])
    formatted = [f"- {r['title']}: {r['content'][:200]}" for r in results[:5]]
    return "\n".join(formatted) if formatted else "No web results found."


if __name__ == "__main__":
    mcp.run(transport="stdio")
