from colorama import Fore, init

# Reset the terminal colors after each print (colorama)
init(autoreset=True)

def printResponse(message: str):
    print(Fore.LIGHTGREEN_EX + message)
    Fore.RESET

def printError(message: str):
    print(Fore.RED + message)
    Fore.RESET


def printSystem(message: str):
    print(Fore.MAGENTA + message)
    Fore.RESET

def printThinking(message: str, end='\n', flush=False):
    print(Fore.LIGHTBLACK_EX + message, end=end, flush=flush)
    Fore.RESET

def printTool(tool: str, message: str):
    print(Fore.LIGHTWHITE_EX + tool + " :: ", end='')
    printSystem(message)
    Fore.RESET

def inputPrompt() -> str:
    return str(input(Fore.LIGHTYELLOW_EX + ">>> ")).strip()