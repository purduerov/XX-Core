import json


class Config(object):
    def __init__(self, root_dir):
        self.root_dir = root_dir

        json_file = open(root_dir + "/install/config.json")
        self.config = json.load(json_file)
        json_file.close()

    def get(self, key):
        """ Return a configuration item from the json
        """
        if key in self.config:
            return self.config[key]
        else:
            return None
