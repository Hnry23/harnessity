from ollama import Client
from harnessity.agentIO import printThinking, printError
from harnessity.config import config

class ModelMessage:
    def __init__(
            self,
            content: str,
            tool_calls: list,
            role: str = 'assistant'
        ):
        self.content = content
        self.tool_calls = tool_calls
        self.role=role

    def to_dict(self) -> dict:
        """Turn the object to dict."""
        msg_dict = {
            "role": self.role,
            "content": self.content
        }
        if self.tool_calls:
            msg_dict["tool_calls"] = self.tool_calls
        return msg_dict

class ModelResponse:
    def __init__(
            self,
            model: str,
            message: ModelMessage,
            done: bool = True,
            stop_reason: str = 'end_turn',
            total_duration = 0,
            load_duration = 0,
            prompt_eval_count = 0,
            eval_count = 0
        ):
        self.model = model
        self.message = message
        self.done = done,
        self.stop_reason = stop_reason
        self.total_duration = total_duration
        self.load_duration = load_duration
        self.prompt_eval_count = prompt_eval_count
        self.eval_count = eval_count

class Model: # TO-DO: Make this model
    def __init__(self, provider: str, name: str, host: str, headers: list):
        self.name = name
        self.host = host
        self.headers = headers
        self.provider = provider
        self.configureProvider()
    
    def configureProvider(self):
        match self.provider:
            case "ollama":
                self.client = Client(
                    host = self.host,
                    headers = self.headers
                )
                self.chat = self.chat_ollama
                return
        printError("Chat not supported in selected provider")

    # OLLAMA :: provider specific chat
    def chat_ollama(self, messages_bag: list, defined_tools: list) -> ModelResponse:
        stream = self.client.chat(
            model=self.name,
            messages=messages_bag,
            tools=defined_tools,
            stream=True
        )
        full_content = ""
        tool_calls = []
        for chunk in stream:
            is_done = chunk.get('done')
            # Capture text content (if any)
            if 'message' in chunk:
                msg = chunk['message']

                # Reconstruct text
                if 'content' in msg:
                    full_content += msg['content']
                    if config.agent.show_thinking and is_done == False:
                        printThinking(msg['content'], end='', flush=True)

                # Reconstruct tool_calls
                if 'tool_calls' in msg:
                    # Ollama use to send the tools in full blocks inside the stream
                    # or accumulate them if the model generates them
                    for t in msg['tool_calls']:
                        tool_calls.append(t)


            # 3. At the end, we reconstruct the "response" object
            if is_done:
                #print a new line (if thinking is being printed)
                if config.agent.show_thinking:
                    printThinking('')
                # prepare the message object
                message = ModelMessage(
                    content=full_content,
                    tool_calls=tool_calls,
                    role='assistant'
                )
                # return the response object
                return ModelResponse(
                    model=chunk.get('model'),
                    message=message,
                    done=True,
                    stop_reason=chunk.get('done_reason', 'stop'),
                    total_duration=chunk.get('total_duration', 0),
                    load_duration=chunk.get('load_duration', 0),
                    prompt_eval_count=chunk.get('prompt_eval_count', 0),
                    eval_count=chunk.get('eval_count', 0)
                )