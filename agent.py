from ollama import Client
from tools import web_search, create_file, read_file, list_folder
from agentIO import printThinking, printError, printSystem, printResponse
import config
import re
import os

# LLM client
client = Client(
  host = config.model_host,
  headers = config.model_headers
)

# Defined tools
defined_tools = [web_search, create_file, read_file, list_folder]

# agent loop
def agent_loop(prompt: str, messages_bag: list = []):
    printThinking(f"Agent loop started, please wait...")

    # First of all, check if there is any context required (with @)
    # It could be: agent, skill or normal file
    required_context = extract_required_context_items(prompt)
    prompt, messages_bag = resolve_context(prompt, messages_bag, required_context)

    printThinking("Thinking...")

    # 1. Inicial history
    messages_bag.append({
        "role": "user",
        "content": prompt
    })
    
    # limit to prevent infinite loop

    MAX_ITERATIONS = 10
    
    for _ in range(MAX_ITERATIONS):
        # 2. Call the LLM
        response = client.chat(
            model=config.model_name,
            messages=messages_bag,
            tools=defined_tools
        )
        
        if hasattr(response, 'message') == False:
            continue

        msg = response.message
        messages_bag.append(msg) # append always the assistant response

        if config.show_thinking and msg.role == 'assistant':
            if msg.thinking != '':
                printThinking(f"{msg.thinking}")
                if msg.content != '':
                    printThinking(f"{msg.content}")

        # 3. If no more tool calls, the agent finished thinking (we break the loop)
        if not msg.tool_calls:
            printResponse(msg.content)
            return response, messages_bag

        # 4. Process 
        for tool_call in msg.tool_calls:
            tool_name = tool_call.function.name
            args = tool_call.function.arguments
            
            # Exect the tool
            result = ""
            match tool_call.function.name:
                case 'load_skill':
                    messages_bag = load_skill(messages_bag = messages_bag, **args)
                case 'list_folder':
                    result = list_folder(**args)
                case 'web_search':
                    result = web_search(**args)
                case 'create_file':
                    result = create_file(**args)
                case 'read_file':
                    result = read_file(**args)
                case _:
                    # Unknown tool
                    continue
                
            # 5. Add the result to the message history if not empty
            if result != "":
                messages_bag.append({
                    "role": "tool",
                    "name": tool_name,
                    "content": str(result)
                })
            
        # loop end (will finish if no more tool calls or MAX_ITERATIONS reached

    printError("The max iteration limit was reached.")
    return response, messages_bag

def count_tokens(response):
    if hasattr(response, 'prompt_eval_count') and hasattr(response, 'eval_count'):
        printSystem(f"Prompt tokens: {response.prompt_eval_count}")
        printSystem(f"Output tokens: {response.eval_count}")
    else:
        printError(f"Error: Eval count not found in provided response: {response}")

def extract_required_context_items(prompt: str) -> list:
    pattern = r"@'(\S+)'"
    return re.findall(pattern, prompt)

def load_skill(messages_bag: list, skill: str) -> list:
    with open(skill, 'r', encoding='utf-8') as f:
        file_content = f.read()
        messages_bag.append({
            "role": "user",
            "content": f"<skill>\n{file_content}</skill>\n"
        })
    return messages_bag

def resolve_context(prompt, messages_bag, required_context) -> list:
    for r in required_context:
        c = r.partition(":")
        match c[0]:
            case 'file'|'skill':
                messages_bag = load_context_file(c[0], c[1], messages_bag)
        prompt = prompt.replace(f"@'{r}'", "")

    return prompt, messages_bag


def load_context_file(tag: str, filename: str, messages_bag: list) -> list:
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