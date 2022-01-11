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

class Load_File():
    def __init__(self, stage, experiment, root_path):
        self.stage      = stage
        self.experiment = experiment
        self.root_path  = root_path
        self.__get_configuration__()
    
    def __get_configuration__(self):
        self.paths    = paths(self.root_path)
        self.config   = self.paths.config[self.stage][self.experiment]
    
    def load_file(self, file='data'):
        fparams   = self.config['files'][file]
        if 'ft_include' in fparams.keys():
            ft_include = fparams.pop('ft_include')
            data       = load_table(**fparams)
            cfeatures  = cvars(data, ft_include)
            data       = data[fparams['sheets'][0]]
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
        