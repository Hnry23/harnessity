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
        prompt_chunks = prompt.split(" ")
        command = prompt_chunks[0]
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
                    printError("You need to start a conversation before you check the context.")
                continue
            case '/agent':
                if len(prompt_chunks) < 2:
                    printError("Agent name not specified.")
                    continue
                success, message_history = Agent.set_agent_definition(prompt_chunks[1], message_history)
                if success == False:
                    printError("There was an error loading the agent.")
                printSystem("Agent loaded.")
                if len(prompt_chunks) < 3:
                    continue
                # We define the rest of the elements as the prompt
                # as we already loaded the agent as a system message
                prompt = " ".join(prompt_chunks[2:])
            case _:
                printError("Unknown command. If you are trying to use a plugin, they will be supported soon.")
                continue

    # If we reach this point we will treat it like a normal prompt (if not empty)
    if prompt != "":
        last_response, message_history = main_agent.agent_loop(prompt, message_history)

printSystem("\nBye!\n")