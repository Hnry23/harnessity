from colorama import Fore, init

# Reset the terminal colors after each print (colorama)
init(autoreset=True)

def printResponse(message: str):
    print(Fore.BLUE + message)
    Fore.RESET

def printError(message: str):
    print(Fore.RED + message)
    Fore.RESET


def printSystem(message: str):
    print(Fore.MAGENTA + message)
    Fore.RESET

def printThinking(message: str):
    print(Fore.LIGHTBLACK_EX + message)
    Fore.RESET

def printTool(message: str):
    print(Fore.YELLOW + message)
    Fore.RESET

def inputPrompt() -> str:
    return str(input(Fore.YELLOW + ">>> ")).strip()