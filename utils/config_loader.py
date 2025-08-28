import json
import os
from kivy.app import App

def load_config(file_path, variable_name=None):
    '''
    Load configuration from a JSON file. If variable_name is provided, it loads the JSON file
    specified by the value of that variable in the initial JSON file.
    '''
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
    '''
    Save configuration to a JSON file. If variable_name is provided, it saves the data to
    the JSON file specified by the value of that variable in the initial JSON file.'''
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
    #print(f"Current page updated to: {page_name}")
    
        
def update_text_language(variable_name=None):
    """
    Update the text language of the application.
    This function should be called when the language is changed.
    """
    app = App.get_running_app()
    if app.language == 'en':
        return app.en_dictionary.get(variable_name, variable_name)
    elif app.language == 'jp':
        return app.jp_dictionary.get(variable_name, variable_name)
        