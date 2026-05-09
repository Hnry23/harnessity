from harnessity.agentCommand import AgentCommand
from harnessity.agentIO import printSystem, printError
from harnessity.agentTools import defined_tools

def get_tools(messages_bag: list, command_prompt: str):
    for tool in defined_tools:
        if callable(tool):
            printSystem(tool.__name__)
        elif isinstance(tool, dict) and 'function' in tool:
            printSystem(tool['function']['name'])
        else:
            printError(f"Wrong tool definition: {tool}")
    return messages_bag, ""
        
commands = [
    AgentCommand('tools', get_tools)
]