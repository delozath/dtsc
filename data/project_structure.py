import re
import yaml

import pdb

class ProjectPaths():
    def __init__(self, script_path, fyaml='config'):
        self.script  = script_path
        self.root    = re.findall(r'(.+?)(?=src)',script_path)[0]
        self.src     = self.root + 'src/'
        self.model   = self.root + 'models/'
        self.images  = self.root + 'images/'
        self.data    = self.root + 'data/'
        self.results = self.root + 'results/'
        self.config  = self.__get_config(fyaml)
    
    def __get_config(self, fyaml):
        #TODO: verify if file exists
        with open(self.src+fyaml+'.yml','r') as fconfig:
            config  = yaml.load(fconfig, Loader=yaml.FullLoader)
        
        return config
    
    def open_yaml(self,file):
        fyaml = self.__get_config(file)
        return fyaml