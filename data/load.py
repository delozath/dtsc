import yaml
import pandas as pd
import pdb

from dtsc.data.structure import paths
from dtsc.data.features  import cvars

def load_table(name, ext, path="./", sheets='none'):
    fname = "{}{}.{}".format(path,name,ext)
    if ext in ['ods', 'xls', 'xlsx']:
        if sheets == 'none':
            sheets = None 
        else:
            sheets = list(sheets)
        
        data = pd.read_excel(fname,sheet_name=sheets)
    elif ext == 'csv':
        data = pd.read_csv(fname, low_memory=False)
    
    elif ext == 'sav':
        data = pd.read_spss(fname)
    
    elif ext in ['ftr', 'fea']:
        data = pd.read_feather(fname)
    
    else:
        data = -1
    
    return data

class __load_context_config__():
    def __init__(self, path, fname_config='config'):
        with open(f'{path}{fname_config}.yml') as yml_file:
            self.available = []
            for read in yaml.safe_load_all(yml_file):
                key = [*read.keys()][0]
                #DeprecationWarning() key=scrubbing
                if   key == 'scrubbing':
                    self.scrubbing = read[key]
                    self.available.append('scrubbing')
                elif key == 'explore':
                    self.explore = read[key]
                    self.available.append('explore')
                elif key == 'ft_selection':
                    self.ft_selection = read[key]
                    self.available.append('ft_selection')
                elif key == 'modeling':
                    self.modeling = read[key]
                    self.available.append('modeling')
                elif key == 'report':
                    self.report = read[key]
                    self.available.append('report')
                #new componenet in yaml file
                elif key == 'data':
                    self.data = read[key]
                    self.available.append('data')                
                elif key == 'params':
                    self.params = read[key]

class load_full_context(__load_context_config__):
    def __init__(self, path, stage):
        super().__init__(path)
        #self.__stages__ = __load_context_config__(path)
        #
        if stage in self.available:
            self.stage = getattr(self, stage)
        else:
            raise ValueError(f'Stage {stage} is not in the yaml configuration file')
        #
        if 'params' in dir(self):
            self.params = self.params
        #
        ## TODO: regresar un objeto con referencia a todo el archivo YAML
    #
    def load(self, process, task):
        fparams = self.stage[process][task]
        full_context_data         = {}
        full_context_vars_include = {}
        for fname_key, fname_params in fparams['load'].items():
            if 'vars_include' in fname_params.keys():
                params       = fname_params.copy()
                vars_include = params.pop('vars_include')
                data         = load_table(**params)
                vars_include = cvars(data, vars_include)
                #
                full_context_data        [fname_key] = data
                full_context_vars_include[fname_key] = vars_include
            else:
                data                         = load_table(**fname_params)
                full_context_data[fname_key] = data
        if not full_context_vars_include:
            full_context_vars_include[fname_key] = 'all'
        return full_context_data, full_context_vars_include