# Functions to be used as agent's tools
import subprocess # To make bash command executions
from ddgs import DDGS # to make DuckDuckGo searches
from output import printTool, printError
import config

def log_tool_usage(tool_name: str, message: str):
    if config.show_tool_usage:
        printTool(f"\n[Tool] {tool_name} :: {message}")

def create_file(file_name: str, content: str):
    """
    Create a file with the provided content and file_name.
    """
    try:
        log_tool_usage("create_file", f"Creating file: {file_name}...")
        with open(file_name, "w") as f:
            f.write(content)
        return "File was succesfully created"
    except Exception as e:
        printError(f"Error creating the file: {e}")
        return f"There was an error creating the file: {e}"

def read_file(file_name: str):
    """
    Read a file.
    """
    try:
        with open(file_name) as f:
            return str(f.read())
    except Exception as e:
        printError(f"Error reading the file: {e}")
        return f"There was an error reading the file: {e}"
        

def web_search(query: str, max_results_to_return: int = config.websearch_max_results) -> str:
    """
    Find on the Internet updated information about any topic.
    Useful for recent news of topics the model does not know.
    Use a higher value in max_results_to_return (default is 3) param to return more results in case a first call was not enough
    """
    log_tool_usage("web_search", f"I am searching the web: {query} with max {max_results_to_return} results...")
    with DDGS() as ddgs:
        # Limit to the first 3 results (to not staturate the context)
        results = [r for r in ddgs.text(query, max_results=max_results_to_return)]
        
    if not results:
        return "No results were found."
    
    # Format the result as a readable text string
    formatted_results = "\n".join([f"Title: {r['title']}\nSummary: {r['body']}\n" for r in results])
    
    return formatted_results

def list_folder(path: str, recursive: bool = False):
    """
    Use this tool to list the content of a folder.
    With recursive as True it will return the content of all subfolders.
    """
    log_tool_usage("list_folder", f"Listing folder: {path}, recursive {recursive}...")
    params = "-lsha"
    if recursive:
        params += "R"

    result = subprocess.run(
        ["ls", params, path],
        capture_output=True,  # Captures stdout y stderr
        text=True # Decode the output
    )
    return result.stdout.strip()


# not exposed functions

def exec_bash_command(command: str, args: str):
    """
    Execute any bash command
    """
    # TODO command and args sanity/security checks
    full_command = command + " " + args
    log_tool_usage("exec_bash_command", f"Executing bash command: {full_command}...")
    
    result = subprocess.check_output(full_command, shell=True, stderr=subprocess.STDOUT)
    return result.decode('utf-8')