import json
import subprocess as sp
import re


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
        paths = sp.Popen("whereis virtualenv", shell=True, stdout=sp.PIPE)
        found = paths.stdout.read()
        found = re.search(r"(?P<venvpath>/.*?/virtualenv)[\n\s$]", found)
        if found:
            return found.group('venvpath')
        else:
            return None
