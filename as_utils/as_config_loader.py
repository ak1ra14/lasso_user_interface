import json, os
from kivy.app import App
from kivy.logger import Logger

def load_config(file_path, variable_name=None,index=0):
    '''
    Load configuration from a JSON file. If variable_name is provided, it loads the JSON file
    specified by the value of that variable in the initial JSON file.
    '''
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        if variable_name:
            next_path = data.get(variable_name)
            #Logger.info(f"Loading config for '{variable_name}' from: {next_path}")
            if isinstance(next_path, list):
                if len(next_path) == 0:
                    return None
                index = 0
                while index < len(next_path):
                    try:
                        # If it's a list, load and return the data from the first file in the list
                        with open(next_path[index], "r") as nf:
                            #Logger.info(f"Loaded config from: {next_path[index-1]}")
                            return json.load(nf)
                    except Exception as e:
                        index += 1
                return None
            elif isinstance(next_path, str):
                # If it's a string, load and return the data from the file
                try:
                    with open(next_path, "r") as nf:
                        return json.load(nf)
                except Exception as e:
                    Logger.exception(f"Failed to load config from {next_path}")
                    return None
            else:
                raise KeyError(f"Variable '{variable_name}' not found in {file_path}")
        else:
            return data
    except Exception as e:
        Logger.exception("Failed to load config")
        raise


def save_config(file_path, variable_name=None, data=None,index=0):
    '''
    Save configuration to a JSON file. If variable_name is provided, it saves the data to
    the JSON file specified by the value of that variable in the initial JSON file.'''
    try:
        with open(file_path,"r") as f:
            paths = json.load(f)
        if variable_name:
            next_path = paths.get(variable_name)
            # If next_path is a list, use the index (default 0)
            if isinstance(next_path, list) and next_path:
                # Find the first existing file in the list
                for target_path in next_path:
                    if os.path.isfile(target_path):
                        with open(target_path, "w") as f:
                            json.dump(data, f, indent=4)
                        return
                # If no file exists, do nothing
                return
            elif isinstance(next_path, str):
                target_path = next_path
            else:
                return  # Do nothing if path is empty or not found
            # Only save if the directory exists and path is not empty
            if target_path and os.path.isdir(os.path.dirname(target_path)):
                with open(target_path, "w") as f:
                    json.dump(data, f, indent=4)
        else:
            if file_path and os.path.isdir(os.path.dirname(file_path)):
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=4)
                return
    except Exception as e:
        Logger.exception("Failed to save config")
        raise

def to_json_format(key, value):
    """
    Convert key-value pair to JSON format
    
    Args:
        key: The key name
        value: The value to be associated with the key
        
    Returns:
        dict: A dictionary in JSON format
        
    Example:
        to_json_format("wifi_ssid", "MyNetwork") 
        returns {"wifi_ssid": "MyNetwork"}
    """
    try:
        json_data = {str(key): value}
        return json_data
    except Exception as e:
        Logger.error(f"ConnectionManager: Error converting to JSON format: {e}")
        return {}

def save_config_partial(file_path, variable_name=None, key=None, value=None, index=0):
    '''
    Save configuration to a JSON file. If variable_name is provided, it saves the data to
    the JSON file specified by the value of that variable in the initial JSON file.
    Only updates specified fields.
    '''
    try:
        data = to_json_format(key,value)
        with open(file_path, "r") as f:
            paths = json.load(f)
        
        if variable_name:
            next_path = paths.get(variable_name)
            if isinstance(next_path, list) and next_path:
                # Find first existing file in list
                for target_path in next_path:
                    if os.path.isfile(target_path):
                        # Read existing data
                        with open(target_path, "r") as f:
                            existing_data = json.load(f)
                        # Update only specified fields
                        existing_data.update(data)
                        # Write back merged data
                        with open(target_path, "w") as f:
                            json.dump(existing_data, f, indent=4)
                        return
                return
            elif isinstance(next_path, str):
                target_path = next_path
                if target_path and os.path.isfile(target_path):
                    # Read existing data
                    with open(target_path, "r") as f:
                        existing_data = json.load(f)
                    # Update only specified fields
                    existing_data.update(data)
                    # Write back merged data
                    with open(target_path, "w") as f:
                        json.dump(existing_data, f, indent=4)
        else:
            if file_path and os.path.isfile(file_path):
                # Read existing data
                with open(file_path, "r") as f:
                    existing_data = json.load(f)
                # Update only specified fields
                existing_data.update(data)
                # Write back merged data
                with open(file_path, "w") as f:
                    json.dump(existing_data, f, indent=4)
    except Exception as e:
        Logger.exception("Failed to save config")
        raise

def update_current_page(page_name):
    """
    Update the current page in the config file.
    """
    config = load_config('as_config/settings.json')
    config['current_page'] = page_name
    save_config('as_config/settings.json', data=config)
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
    
def read_txt_file(file_path):
    """
    Read and return the contents of a text file.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    

def get_valid_value(config, key,default):
    if config and key in config:
        return config[key]
    return default


def check_all_values_same(file_path, variable_name='location_json',key=None,value_to_check=None):
    with open(file_path, "r") as f:
        data = json.load(f)
    if variable_name:
        next_path = data.get(variable_name)
    all_same = True
    if isinstance(next_path, list):
        for path in next_path:
            with open(path, "r") as f:
                config = json.load(f)
                value = config.get(key, None)
            if value != value_to_check:
                return False
    return all_same

def update_all_values(file_path, variable_name='location_json', key=None, new_value=None):
    with open(file_path, "r") as f:
        data = json.load(f)
    if variable_name:
        next_path = data.get(variable_name)
    if isinstance(next_path, list):
        for path in next_path:
            with open(path, "r") as f:
                config = json.load(f)
            config[key] = new_value
            with open(path, "w") as f:
                json.dump(config, f, indent=4)


        