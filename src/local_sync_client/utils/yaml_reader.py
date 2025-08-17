from yaml import safe_load

class YamlReader:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.config = self._read_config()
    
    # Read the whole yaml file, and returnes it as a dictionary
    def _read_config(self):
        with open(self.file_path, 'r') as file:
            config_file = safe_load(file)
        return config_file
    
    # Finds the username in the yaml file, if it exists return config dictionary for the user
    def get_config_username(self, username: str):
        for user in self.config['local_sync_client']['users']:
            if user['username'] == username:
                return user
        


