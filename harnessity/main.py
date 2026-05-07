from harnessity.commands import agent_commands
from harnessity.model import Model
from harnessity.agent import Agent
from harnessity.agentIO import printError, inputPrompt, printSystem
from harnessity.config import config
from harnessity.agentMCP import initConfiguredMCP, getMCPTools
from harnessity.agentTools import defined_tools

# LLM client
model = Model(
    provider = config.model.provider,
    name = config.model.name,
    host = config.model.host,
    headers = config.model.headers
)

def main():
    printSystem("\nAI agent\n========\n")

    # MCP tools
    initConfiguredMCP()
    defined_tools.extend(getMCPTools())

    main_agent = Agent(model, defined_tools)

    loop = True
    message_history = []
    last_response = None

    while loop:
        try:
            prompt = ""
            prompt = inputPrompt()
        except Exception as e:
            printError("An unexpected error hapenned, please try again.")
            continue

        if prompt == "":
            continue

        # Is it a command call?
        if prompt[0] == '/':
            prompt_chunks = prompt[1:].split(" ", 1)
            command = prompt_chunks[0]
            command_prompt = None
            if len(prompt_chunks)>1:
                prompt_chunks[1]

            match command:
                case 'exit'|'bye'|'quit':
                    break
                case 'clear':
                    message_history = []
                    last_response = None
                    continue
                case 'context':
                    if last_response != None:
                        main_agent.count_tokens(last_response)
                    else:
                        printError("You need to start a conversation before you check the context.")
                    continue
                case _:
                    if command in agent_commands and callable(agent_commands[command]):
                        printSystem(f"Executing command... {agent_commands[command].name}")
                        message_history, prompt = agent_commands[command](message_history, command_prompt)
                    else:
                        printError("Unknown command. If you are trying to use a plugin, they will be supported soon.")
                        continue

        # If we reach this point we will treat it like a normal prompt (if not empty)
        if prompt != "":
            last_response, message_history = main_agent.agent_loop(prompt, message_history)

    printSystem("\nBye!\n")