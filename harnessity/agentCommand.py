# Class for commands
class AgentCommand:
    def __init__(self, name: str, accion):
        self.name = name
        self.accion = accion

    def __call__(self, messages_history: list, command_prompt: str):
        messages_history, command_prompt = self.accion(messages_history, command_prompt)
        if command_prompt == None:
            command_prompt = ""
        return messages_history, command_prompt
    


