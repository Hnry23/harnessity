# Model
model_host = 'http://192.168.1.95:11434'
model_name = 'gemma4:custom'
model_headers = {'x-some-header': 'some-value'}

# Agent
show_thinking = True # Show/hide the thinking process

# Tool
show_tool_usage = True # prints a line everytime a tool is being used
websearch_max_results = 5 # default value, can be overriden by the model

# System prompt
system_prompt = '"""' \
'' \
'"""'