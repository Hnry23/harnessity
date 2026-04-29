from ollama import Client

class Model:
    def __init__(self, provider: str, name: str, host: str, headers: list):
        self.name = name
        self.host = host
        self.headers = headers
        self.provider = provider

        self.client = self.getClient()
    
    def chat(self, messages_bag: list, defined_tools: list):
        return self.client.chat(
            model=self.name,
            messages=messages_bag,
            tools=defined_tools
        )
    
    def getClient(self) -> Client:
        if self.provider == "ollama":
            return Client(
                host = self.host,
                headers = self.headers
            )