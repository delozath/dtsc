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
            full_context_vars_include['include'] = 'all'
        return full_context_data, full_context_vars_include
        


#DeprecationWarning()
class Load_File():
    def __init__(self, stage, experiment, root_path):
        self.stage      = stage
        self.experiment = experiment
        self.root_path  = root_path
        self.__get_configuration__()
    
    def __get_configuration__(self):
        self.paths  = paths(self.root_path)
        self.config = self.paths.config[self.stage][self.experiment]
        
        if 'params' in self.paths.config.keys():
            self.params = self.paths.config['params']
    
    def load_file(self, file='data', fparams=0):
        if fparams==0:
            fparams   = self.config['files'][file]
        
        return self.__load_file__(file=file, fparams=fparams)
    
    def __load_file__(self, fparams, file='data'):
        if 'ft_include' in fparams.keys():
            ft_include = fparams.pop('ft_include')
            data       = load_table(**fparams)
            cfeatures  = cvars(data, ft_include)
            
            if 'features' in data.keys():
                data.pop('features')
                
                sheets = list(data.keys())
                if len(sheets)==1:
                    data   = data[sheets[0]]
            
            return data, cfeatures, ft_include
        
        #Deprecated: caso para compatibilidad 
        elif 'feature_groups' in fparams.keys(): 
            ft_include = fparams.pop('feature_groups')
            data       = load_table(**fparams)
            cfeatures  = cvars(data, ft_include)
            data       = data[fparams['sheets'][0]]
            return data, cfeatures, ft_include
        
        else:
            data       = load_table(**fparams)
            return data
    
    #Return keys of available file parameters for loading
    def files(self):
        files = self.config['files'].keys()
        return list(files)
    
    def get_output_fname(self,fout='target'):
        #create output file name (joined file)
        fparms = self.loader.config['files'][fout]
        if 'path' in fparms.keys():
            out = f"{fparms['path']}{fparms['name']}.{fparms['ext']}"
        else:
            path = self.loader.paths.data
            out  = '.'.join(self.loader.config['files'][fout].values())
            out  = path + out
        
        return out
        