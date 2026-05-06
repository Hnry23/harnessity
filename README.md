# 🤖 Harnessity

**Harnessity** is an experimental playground designed to explore the synergy between Large Language Models (LLMs) and the real world. This project acts as a **harness and agent** that provides LLMs with a set of tools to interact with your system, effectively multiplying their capabilities through a modular and extensible architecture.

> [!IMPORTANT]  
> This is a **purely educational and "just for fun" project**. It is built as a sandbox to experiment with agentic behaviors, tool-use, and the Model Context Protocol (MCP). It is not intended for production use, but rather as a creative way to see how far an LLM can go when given a "pair of hands" to interact with a computer.

## ✨ Features

*   **LLM Agent:** A core system for orchestrating LLM interactions and reasoning loops.
*   **Tool Integration:** Built-in tools (web search, file operations) and dynamic extension via the **Model Context Protocol (MCP)**.
*   **Contextual Awareness:** Support for loading context from files or specific "skills" to guide the agent.
*   **Interactive CLI:** A simple and fun command-line interface to manage your sessions and agents.


## ⚙️ Project Structure

The application is organized into modular components:

*   `main.py`: Entry point. Initializes the LLM client, the Agent, and the command loop.
*   `agent.py`: Core logic for the `Agent` class (reasoning loops and tool execution).
*   `model.py`: Interface for underlying LLMs (e.g., Ollama, OpenAI).
*   `agentIO.py`: Standardized input/output (UI, errors, and "thinking" states).
*   `agentTools.py`: Built-in tools (`web_search`, `create_file`, `read_file`, `list_folder`).
*   `agentMCP.py`: MCP integration for external tool servers.
*   `config.json.dist`: Template for LLM connections and agent parameters.
*   `skills/`: Directory for custom skills and context files.

---

## 🚀 Setup Instructions

### 1. Configuration
Before running the application, you must configure your environment:
1.  Copy the template file:
```bash
cp config.json.dist config.json
```
2.  Edit `config.json` with your LLM provider details (host, model name, API keys, etc.).

### 2. Installation
Using a virtual environment is highly recommended to avoid conflicts with system libraries (especially on **macOS/Homebrew** and modern **Linux** distributions via PEP 668).

#### Clone the repository
```bash
git clone https://github.com
cd harnessity
```

#### Set up a Virtual Environment (Recommended)

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```powershell
python -m venv .venv
.venv\(\Scripts\activate \%\%\)MAGIT_PARSER_PROTECT%%
```

**Note for macOS/Linux users:** If you see an `externally-managed-environment` error, it is because your system protects the global Python installation. Please use the virtual environment method above or install via `pipx`.

#### Install the package
Once the environment is active, install the package in **editable mode**:
```bash
pip install -e .
```
This registers the `harnessity` command globally within your environment and installs all required dependencies automatically.

---

## 🗣️ Usage & Commands

Run the tool from any directory in your terminal by simply typing:
```bash
harnessity
```
The application will process files in your current working directory while correctly accessing its internal resources.

### Agent Commands
The agent is controlled via specific slash commands entered at the prompt:


| Command | Description | Example |
| :--- | :--- | :--- |
| **/exit**, **/quit** | Terminates the agent session and exits. | `/exit` |
| **/clear** | Resets the message history and session state. | `/clear` |
| **/context** | Displays token usage and interaction stats. | `/context` |
| **/agent [name]** | Loads a predefined agent from `./agents/`. | `/agent Coder "Fix this bug"` |

---

## 🛠️ Maintenance & Uninstallation

**Verify Installation:**
To check if the dependencies were installed correctly, you can run:
```bash
pip check
```

**Uninstallation:**
If you wish to remove the command and the package from your system:
```bash
pip uninstall harnessity
```
