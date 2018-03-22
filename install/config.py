import json
import os
import re
from pprint import pprint as pp


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
    def findVenv(self):
        os.system("whereis virtualenv > foundit.txt")
        with open('foundit.txt', 'r') as fp:
            found = fp.read()
        os.system("rm foundit.txt")
        pp(found)
        found = re.search(r"(?P<venvpath>/.*/virtualenv)[\n\s]", found)
        if found:
            return found.group('venvpath')
        else:
            return None


if __name__ == "__main__":
    c = Config('./')
    c.findVenv()
