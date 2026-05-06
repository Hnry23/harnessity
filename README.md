# 🤖 Harnessity

This project is an application designed to serve as a **harness and agent** that communicates with Large Language Models (LLMs) and provides them with tools and access to the real world to multiply their capabilities. It is designed to be a versatile platform extending beyond simple software development tasks.

## ✨ Features

*   **LLM Agent:** A core system for orchestrating LLM interactions.
*   **Tool Integration:** Agents can be equipped with built-in tools (e.g., web search, file operations) and dynamically extended via the Model Context Protocol (MCP) to interact with external servers.
*   **Contextual Awareness:** The system supports loading context from files or skills to inform the agent's decisions.
*   **Interactive CLI:** A command-line interface for interacting with the agent and managing the session.

## ⚙️ Project Structure & Setup

The project is organized around several Python scripts that define the core components:

*   `main.py`: The entry point of the application, which initializes the LLM client, the Agent, and runs the main command loop.
*   `agent.py`: Contains the core logic for the `Agent` class, handling the LLM calls, tool execution, and the agent loop.
*   `model.py`: Defines the `Model` class responsible for interfacing with the underlying LLM (e.g., Ollama).
*   `agentIO.py`: Provides helper functions for standardized output (printing responses, errors, thinking states) and user input.
*   `agentTools.py`: Defines the set of built-in external functions (tools) that the agent can call (e.g., `web_search`, `create_file`, `read_file`, `list_folder`).
*   `agentMCP.py`: Handles Model Context Protocol (MCP) integration, allowing the agent to connect to external servers for additional tools.
*   `config.json` / `config.json.dist`: Configuration files for setting up the LLM connection, agent parameters, and MCP servers.
*   `skills/`: A directory where custom skills/context files can be stored.

### 🚀 Setup Instructions

1.  **Configuration:** Before running the application, you must configure the system.
    *   Copy the template file: **`config.json.dist`** to **`config.json`**.
    *   Edit the resulting `config.json` to set up your LLM provider details (e.g., Ollama host, model name, headers).

2.  **Environment:** The project relies on a virtual environment:
    *   Create and activate the environment: `python -m venv .venv`
    *   Activate: `source .venv/bin/activate` (or `.venv\Scripts\activate` on Windows)

3.  **Execution:** For CLI usage, the entry point of the project is `main.py`. Run the main application script:
    *   `python main.py`

## 🗣️ Agent Commands

The agent is designed to be controlled via specific commands entered at the prompt.

| Command | Description | Usage Example |
| :--- | :--- | :--- |
| **/exit**, **/bye**, or **/quit** | Terminates the agent session and exits the program. | `/exit` |
| **/clear** | Clears the current message history and resets the session state. | `/clear` |
| **/context** | Displays the token usage statistics from the previous interaction. | `/context` |
| **/agent [name] [rest of prompt]** | Loads a predefined agent definition from the `./agents/` folder and sets it as the system instruction. | `/agent MyAgent "What is the capital of France?"` |

### 💡 How to Use Commands

When interacting with the agent, start your input with the command prefix:

*   **To exit:** Type `/exit` and press Enter.
*   **To clear history:** Type `/clear` and press Enter.
*   **To check context:** Type `/context` and press Enter.
*   **To load an agent:** Use the `/agent` command followed by the agent's name and the rest of your request.

## 📚 Code Overview

The system is built upon a modular design:

*   **`model.py`**: Manages the connection and communication with the external LLM.
*   **`agentTools.py`**: Defines the set of built-in functions the agent can invoke to interact with the external environment.
*   **`agentMCP.py`**: Integrates Model Context Protocol (MCP) to dynamically load tools from external servers.
*   **`agent.py`**: Implements the core agent logic, including the multi-step reasoning loop and tool execution.
*   **`main.py`**: Orchestrates the entire process, handling user input and managing the agent lifecycle.