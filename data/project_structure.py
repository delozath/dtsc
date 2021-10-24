import re
import yaml

import pdb

class ProjectPaths():
    def __init__(self, script_path, query):
        self.script  = script_path
        self.root    = re.findall(r'(.+?)(?=src)',script_path)[0]
        self.src     = self.root + 'src/'
        self.model   = self.root + 'models/'
        self.images  = self.root + 'images/'
        self.data    = self.root + 'data/'
        self.results = self.root + 'results/'
        self.config  = self.__get_config(query)
    
    def __get_config(self, query, fname='config.yml'):
        #TODO: verify if file exists
        with open(self.src+fname,'r') as fconfig:
            config  = yaml.load(fconfig, Loader=yaml.FullLoader)
        
        return config[query['stage']][query['experiment']]
    
    def open_config(self,fname,query):
        return self.__get_config(query,fname)