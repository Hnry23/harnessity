import base64

from harnessity.config import config
from harnessity.agentIO import printTool, printError

import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

configured_mcps = {}

def initConfiguredMCP():   
    for mcp_item in config.mcp.servers:
        configured_mcps[mcp_item['name']] = MCPInstance(
            name=mcp_item['name'],
            host=mcp_item['host'],
            api_key=mcp_item['api_key']
        )

def getMCPTools() -> list:
    tools = []
    for mcp_item in configured_mcps:
        tmp = configured_mcps[mcp_item].tools()
        if len(tmp) > 0:
            tools.extend(tmp)
    return tools

def executeMCPTool(mcpName: str, toolName: str, **params):
    if mcpName not in configured_mcps:
        return "The tool could not be found"
    
    mcp = configured_mcps[mcpName]

    logMCPUsage(mcp_name=mcpName, tool_name=toolName, message=f'Execute mcp with params: {params}')
    try:
        response = asyncio.run(mcp.call_tool(toolName, params))
        return response.content
    except Exception as e:
        printError(f"Error calling MCP tool: {e}")
        return f"Error: {str(e)}"

def logMCPUsage(mcp_name: str, tool_name: str, message: str):
    if config.mcp.show_usage:
        printTool(f"\n[MCP] {mcp_name} :: {tool_name} :: {message}")

class MCPInstance:
    name: str
    host: str
    api_key: str

    def __init__(self, name: str, host: str, api_key: str):
        self.name = name
        self.host = host
        self.api_key = api_key

    def get_headers(self) -> str:
        headers = {}
        if self.api_key != "":
            auth_bytes = f"hnry23@gmail.com:{self.api_key}".encode("utf-8")
            auth_b64 = base64.b64encode(auth_bytes).decode("utf-8")
            headers["Authorization"] = f"Basic {auth_b64}"
            headers["Content-Type"] = "application/json"
        return headers

    def tools(self) -> list:
        tools = []
        tools_mcp = asyncio.run(self.retrieve_tools())
        for tool in tools_mcp:
            tool_dict = {
                "type": "function",
                "function": {
                    "name": f'mcp|{self.name}|{tool.name}',
                    "description": tool.description,
                    "parameters": tool.inputSchema, # MCP uses JSON Schema here
                }
            }
            tools.append(tool_dict)
        return tools
    
    async def retrieve_tools(self):
        tools = []
        async with sse_client(self.host, headers=self.get_headers()) as (read, write):
            async with ClientSession(read, write) as session:
                # Init connection
                await session.initialize()
                # List tools
                tools = await session.list_tools()
        if hasattr(tools, 'tools'):
            tools = tools.tools
        return tools
    
    async def call_tool(self, tool_name: str, arguments: dict):
        async with sse_client(self.host, headers=self.get_headers()) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                # call
                result = await session.call_tool(tool_name, arguments)
                return result