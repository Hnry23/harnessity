import os
import importlib.util

def load_commands():
    command_list = {}
    folder = os.path.join(os.path.dirname(__file__), 'commands/')
    
    # List files in commands folder
    for filename in os.listdir(folder):
        # Filter by prefix and extension
        if filename.startswith("command_") and filename.endswith(".py"):
            module_name = filename[:-3]  # Remove the extension (.py)
            ruta_completa = os.path.join(folder, filename)
            
            # Config dynamic load
            spec = importlib.util.spec_from_file_location(module_name, ruta_completa)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Check if variable 'command' exists and we add it
            if hasattr(module, 'commands'):
                if isinstance(module.commands, list):
                    for c in module.commands:
                        command_list[c.name] = c
                
    return command_list


agent_commands = load_commands()