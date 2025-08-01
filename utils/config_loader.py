import json
import os

def load_config(file_path, variable_name=None):
    with open(file_path, "r") as f:
        data = json.load(f)
    if variable_name:
        # Get the path from the variable in the config
        next_path = data.get(variable_name)
        if next_path:
            with open(next_path, "r") as nf:
                return json.load(nf)
        else:
            raise KeyError(f"Variable '{variable_name}' not found in {file_path}")
    else:
        with open(file_path, "r") as f:
            data = json.load(f)
    return data

def save_config(file_path, variable_name=None, data=None):
    with open(file_path,"r") as f:
        paths = json.load(f)
    if variable_name:
        try:
            next_path = paths.get(variable_name)
            if next_path:
                with open(next_path, "w") as f:
                        json.dump(data, f, indent=4)
        except:
            raise KeyError(f"Variable '{variable_name}' not found in {file_path}")
    else:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
            return
        
def update_current_page(page_name):
    """
    Update the current page in the config file.
    """
    config = load_config('config/settings.json')
    config['current_page'] = page_name
    save_config('config/settings.json', data=config)
    print(f"Current page updated to: {page_name}")
