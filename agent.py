from ollama import Client
from tools import web_search, create_file, read_file, list_folder
from output import printThinking, printError, printSystem, printResponse
import config
import re

# LLM client
client = Client(
  host = config.model_host,
  headers = config.model_headers
)

# Defined tools
defined_tools = [web_search, create_file, read_file, list_folder]

# agent loop
def agent_loop(prompt: str, messages_bag = []):
    printThinking(f"Agent loop started, please wait...")

    # First of all, check if there is any context required (with @)
    # It could be: agent, skill or normal file
    required_context = extract_required_context_items(prompt)
    prompt, messages_bag = resolve_context(prompt, messages_bag, required_context)

    printThinking("Thinking...")

    # 1. Inicial history
    messages_bag.append({"role": "user", "content": prompt})
    
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
                
            # 5. Add the result to the message history
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

def resolve_context(prompt: str, messages_bag: list, require_context: list):
    printThinking(f"Resolving context items...")
    for c in require_context:
        string_to_remove = "@'" + c + "'"
        prompt = prompt.replace(string_to_remove, "")
        temp = c.partition(":")
        match temp[0]:
            case 'agent':
                continue
            case 'skill':
                continue
            case 'file':
                continue
    return prompt, messages_bag