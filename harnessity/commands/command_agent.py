from harnessity.agentCommand import AgentCommand
from harnessity.agentIO import printError, printSystem

def load_agent(messages_bag: list, prompt: str):
    if prompt == None or len(prompt) == 0:
        printError("Agent name not specified.")
        return messages_bag, ""
    
    prompt_chunks = prompt.split(" ",1)
    success, messages_bag = set_agent_definition(prompt_chunks[1], messages_bag)
    if success == False:
        printError("There was an error loading the agent.")
        return messages_bag, ""
    
    printSystem("Agent loaded.")
    if len(prompt_chunks) < 2:
        return messages_bag, ""

    return messages_bag, prompt_chunks[1]
                      
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


commands = [AgentCommand('agent', load_agent)]