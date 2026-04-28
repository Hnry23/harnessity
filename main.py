from agent import agent_loop, count_tokens
from agentIO import printError, inputPrompt, printSystem

printSystem("\nAI agent\n========\n")

loop = True
message_history = []
last_response = None

while loop:
    prompt = None
    prompt = inputPrompt()

    if prompt == None:
        continue

    # Is it a command call?
    if prompt[0] == '/':
        prompt = prompt.partition(" ")
        command = prompt[0]
        match command:
            case '/exit'|'/bye':
                break
            case '/clear':
                message_history = []
                last_response = None
                continue
            case '/context':
                if last_response != None:
                    count_tokens(last_response)
                else:
                    printError("You need to start a conversation before you check the context")
                continue
            case _:
                printError("Unknown command. If you are trying to use a plugin, they will be supported soon.")
                continue
        continue

    # If we reach this point we will treat it like a normal prompt
    last_response, message_history = agent_loop(prompt, message_history)

printSystem("\nBye!\n")