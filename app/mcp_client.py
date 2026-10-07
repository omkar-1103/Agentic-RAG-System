import json
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from app.utils.logger import logger


class MCPToolClient:
    """Connects to MCP Servers and dynamically discovers and calls their tools."""

    def __init__(self, config_path="mcp_config.json"):
        with open(config_path) as f:
            self.config = json.load(f)

    async def call_tool(self, server_name: str, tool_name: str, arguments: dict) -> str:
        """Call a specific tool on a specific MCP server."""
        server_config = self.config["mcpServers"][server_name]
        server_params = StdioServerParameters(
            command=server_config["command"],
            args=server_config["args"]
        )

        logger.info(f"[MCP Client] Calling tool '{tool_name}' on server '{server_name}'")

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result.content[0].text

    async def list_tools(self, server_name: str) -> list:
        """Discover all available tools on a specific MCP server."""
        server_config = self.config["mcpServers"][server_name]
        server_params = StdioServerParameters(
            command=server_config["command"],
            args=server_config["args"]
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                return [
                    {"name": tool.name, "description": tool.description}
                    for tool in tools.tools
                ]

    def call_tool_sync(self, server_name: str, tool_name: str, arguments: dict) -> str:
        """Synchronous wrapper for call_tool, for use inside LangGraph nodes."""
        return asyncio.run(self.call_tool(server_name, tool_name, arguments))
