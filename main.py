from model import Model
from agent import Agent
from agentIO import printError, inputPrompt, printSystem
from config import config
import tools

printSystem("\nAI agent\n========\n")

# LLM client
model = Model(
    provider = config.model.provider,
    name = config.model.name,
    host = config.model.host,
    headers = config.model.headers
)

# Defined tools
defined_tools = [
    tools.web_search,
    tools.create_file,
    tools.read_file,
    tools.list_folder
]

main_agent = Agent(model, defined_tools)

loop = True
message_history = []
last_response = None

while loop:
    prompt = ""
    prompt = inputPrompt()

    if prompt == "":
        continue

    # Is it a command call?
    if prompt[0] == '/':
        prompt = prompt.partition(" ")
        command = prompt[0]
        match command:
            case '/exit'|'/bye'|'/quit':
                break
            case '/clear':
                message_history = []
                last_response = None
                continue
            case '/context':
                if last_response != None:
                    main_agent.count_tokens(last_response)
                else:
                    printError("You need to start a conversation before you check the context")
                continue
            case '/agent':
                printSystem("To be implemente...")
                continue
            case _:
                printError("Unknown command. If you are trying to use a plugin, they will be supported soon.")
                continue
        continue

    # If we reach this point we will treat it like a normal prompt (if not empty)
    if prompt != "":
        last_response, message_history = main_agent.agent_loop(prompt, message_history)

printSystem("\nBye!\n")