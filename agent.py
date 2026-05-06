from model import Model
from agentTools import web_search, create_file, read_file, list_folder
from agentIO import printThinking, printError, printSystem, printResponse
from config import config
from agentMCP import executeMCPTool
import re
import os

class Agent:

    def __init__(self, model: Model, defined_tools: list):
        self.defined_tools = defined_tools
        self.model = model
        self.client = model.getClient()

    # agent loop
    def agent_loop(self, prompt: str, messages_bag: list = []):
        printThinking(f"Agent loop started, please wait...")

        # First of all, check if there is any context required (with @)
        # It could be: agent, skill or normal file
        required_context = self.extract_required_context_items(prompt)
        prompt, messages_bag = self.resolve_context(prompt, messages_bag, required_context)

        # 0. keep original messages before starting (just in case)
        original_messages_bag = messages_bag

        # 1. Inicial history
        messages_bag.append({
            "role": "user",
            "content": prompt
        })
        
        for _ in range(config.agent.max_loop_iterations):
            # Clean the history if needed
            self.prune_history(messages_bag=messages_bag, max_messages=config.agent.max_messages)

            # 2. Call the LLM
            try:
                response = self.model.chat(messages_bag, self.defined_tools)
            except Exception as e:
                printError(f"Error connecting to the model: {e}")
                return original_messages_bag
            
            if hasattr(response, 'message') == False:
                continue

            msg = response.message
            messages_bag.append(msg) # append always the assistant response

            # Stop reason handling
            stop_reason = getattr(response, 'stop_reason', None)
            if stop_reason == "max_tokens":
                printError("Warning: Context window or output limit reached (max_tokens).")
                return None, messages_bag
            if stop_reason == "content_filter":
                printError("Warning: The response was blocked by content filters.")
                return None, messages_bag

            if config.agent.show_thinking and msg.role == 'assistant':
                if msg.thinking != '':
                    printThinking(f"{msg.thinking}")
                    if msg.content != '':
                        printThinking(f"{msg.content}")

            # 3. If end turn or no more tool calls, the agent finished thinking (we break the loop)
            if stop_reason == "end_turn" or not msg.tool_calls:
                printResponse(msg.content)
                return None, messages_bag

            # 4. Process tool calling (mcp and local tools)
            for tool_call in msg.tool_calls:
                tool_name = tool_call.function.name
                args = tool_call.function.arguments

                # Execute the MCP tool (if is a MCP request)
                result = self.execute_tool(messages_bag=messages_bag, tool_name=tool_name, **args)
                    
                # 5. Add the result to the message history
                messages_bag.append({
                    "role": "tool",
                    "name": tool_name,
                    "content": str(result)
                })

        printError("The max iteration limit was reached.")
        return response, messages_bag

    def execute_tool(self, messages_bag: list, tool_name:str, **args) -> tuple[list, str]:
        if tool_name.startswith("mcp|"):
            parts = tool_name[4:].split("|", 1)
            if len(parts) == 2:
                mcp_name_real, tool_name_real = parts
                result = executeMCPTool(mcpName=mcp_name_real, toolName=tool_name_real, **args)
            else:
                result = "Error: The tool is not correctly named"
        else:
            # Execute the tool
            match tool_name:
                case 'load_skill':
                    messages_bag = self.load_skill(messages_bag = messages_bag, **args)
                case 'list_folder':
                    result = list_folder(**args)
                case 'web_search':
                    result = web_search(**args)
                case 'create_file':
                    result = create_file(**args)
                case 'read_file':
                    result = read_file(**args)
                case _:
                    result = "Tool not available"
        return messages_bag, result

    def count_tokens(self, response):
        if hasattr(response, 'prompt_eval_count') and hasattr(response, 'eval_count'):
            printSystem(f"Prompt tokens: {response.prompt_eval_count}")
            printSystem(f"Output tokens: {response.eval_count}")
        else:
            printError(f"Error: Eval count not found in provided response: {response}")

    def extract_required_context_items(self, prompt: str) -> list:
        pattern = r"@'(\S+)'"
        return re.findall(pattern, prompt)

    def load_skill(self, messages_bag: list, skill: str) -> list:
        with open(skill, 'r', encoding='utf-8') as f:
            file_content = f.read()
            messages_bag.append({
                "role": "system",
                "content": f"<skill>\n{file_content}</skill>\n"
            })
        return messages_bag

    def resolve_context(self, prompt, messages_bag, required_context) -> list:
        for r in required_context:
            c = r.partition(":")
            match c[0]:
                case 'file'|'skill':
                    messages_bag = self.load_context_file(c[0], c[1], messages_bag)
            prompt = prompt.replace(f"@'{r}'", "")

        return prompt, messages_bag

    def load_context_file(self, tag: str, filename: str, messages_bag: list) -> list:
        if os.path.exists(filename) != True:
            printError(f"The required file cannot be found: {filename}")
        else:
            with open(filename, 'r', encoding='utf-8') as f:
                file_content = f.read()
                messages_bag.append({
                    "role": "user",
                    "content": f"<{tag}>\n{file_content}</{tag}>\n"
                })
        
        return messages_bag
    
    def prune_history(self, messages_bag: list, max_messages: int = 10) -> list:
        # Keep the system prompts and last {max_messages} messages
        if len(messages_bag) > max_messages:
            printSystem(f"Cleaning history: Keeping last {max_messages} messages.")
            system_prompt = [m for m in messages_bag if m['role'] == 'system']
            recent_context = messages_bag[-(max_messages-len(system_prompt)):]
            return system_prompt + recent_context
        return messages_bag

    @staticmethod
    def set_agent_definition(agent_name: str, messages_bag: list) -> tuple[bool, list]:
        filename = "./agents/" + agent_name + ".md"
        if os.path.exists(filename) != True:
            printError(f"The required agent definition cannot be found: {agent_name}")
            return False, messages_bag
        with open(filename, 'r', encoding='utf-8') as f:
            file_content = f.read()
            messages_bag.append({
                "role": "system",
                "content": file_content
            })
        return True, messages_bag
