from config import config
from agentIO import printTool, printError

import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

configured_mcps = []

def initConfiguredMCP():   
    for mcp_item in config.mcp.servers:
        configured_mcps.append(MCPInstance(
            name=mcp_item['name'],
            protocol=mcp_item['protocol'],
            host=mcp_item['host'],
            port=mcp_item['port']
        ))

def getMCPTools() -> list:
    tools = []
    for mcp_item in configured_mcps:
        tmp = mcp_item.tools()
        if len(tmp) > 0:
            tools.extend(tmp)
    return tools

def executeMCPTool(mcpName: str, toolName: str, **params):
    logMCPUsage(mcp_name=mcpName, tool_name=toolName, message=f'Execute mcp with params: {params}')
    return "10 employees"

def logMCPUsage(mcp_name: str, tool_name: str, message: str):
    if config.mcp.show_usage:
        printTool(f"\n[MCP] {mcp_name} :: {tool_name} :: {message}")

class MCPInstance:
    name: str
    protocol: str
    host: str
    port: int
    url: str

    def __init__(self, name: str, protocol: str, host: str, port: int):
        self.name = name
        self.protocol = protocol
        self.host = host
        self.port = port
        self.url = f'{self.protocol}://{self.host}:{self.port}/sse'

    def tools(self) -> list:
        tools = []
        tools_mcp = asyncio.run(self.retrieve_tools())
        for tool in tools_mcp:
            tool_dict = {
                "type": "function",
                "function": {
                    "name": f'mcp_{self.name}_{tool.name}',
                    "description": tool.description,
                    "parameters": tool.inputSchema, # MCP uses JSON Schema here
                }
            }
            tools.append(tool_dict)
        return tools
    
    async def retrieve_tools(self):
        tools = []
        async with sse_client(self.url) as (read, write):
            async with ClientSession(read, write) as session:
                # Init connection
                await session.initialize()
                
                # List tools
                tools = await session.list_tools()

        if hasattr(tools, 'tools'):
            tools = tools.tools

        return tools