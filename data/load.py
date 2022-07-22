import yaml
import pandas as pd
import pdb

from dtsc.data.structure import paths
from dtsc.data.features  import cvars

import re
import yaml

import os.path


import pdb

class project_structure():
    def __init__(self, project_path):
        self.script  = project_path
        self.root    = re.findall(r'(.+?)(?=src)',project_path)[0]
        self.src     = self.root + 'src/'
        self.models  = self.root + 'models/'
        self.images  = self.root + 'images/'
        self.data    = self.root + 'data/'
        self.results = self.root + 'results/'
#
#
class load_project():
    FNAME_MANIFEST = 'config'
    STAGE_DATA     = 'data'
    LOADING_KEY    = 'load'
    #
    KEY_VARS            = 'variables'
    KEY_VARS_DEPRECATED = 'features'
    def __init__(self, project_path, block, stage, task):
        self.structure = project_structure(project_path)
        self.config    = self.__load_manifest()
    #
    #
    @staticmethod
    def load_table(name, ext, path="./", sheets='none'):
        fname = f"{path}{name}.{ext}"
        if ext in ['ods', 'xls', 'xlsx']:
            if sheets == 'none':
                sheets = None 
            else:
                sheets = list(sheets)
            #
            data = pd.read_excel(fname,sheet_name=sheets)
        elif ext == 'csv':
            data = pd.read_csv(fname, low_memory=False)
        #
        elif ext == 'sav':
            data = pd.read_spss(fname)
        #
        elif ext in ['ftr', 'fea']:
            data = pd.read_feather(fname)
        #
        else:
            data = None
        #
        return data
    #
    @classmethod
    def from_manifest(cls, project_path, block, stage, task):
        instance = cls(project_path, block, stage, task)
        #
        if stage in instance.config[instance.STAGE_DATA].keys():
            config_stage = instance.config[instance.STAGE_DATA][stage]
            if  task in config_stage.keys():
                config_task = config_stage[task]
                if cls.LOADING_KEY in config_task.keys():
                    dbs_info = config_task[cls.LOADING_KEY]
                    #
                    data, vars_include = instance.__load_data_with_manifest(dbs_info)
                    #
                    db_names = [*data.keys()]
                    if len(db_names)>1:
                        instance.data_db = data
                    elif len(db_names)==1:
                        instance.data_db = data[db_names]
                    #
                    vars_inc      = {}
                    data_vars_inc = {}
                    for key, vars in vars_include.items():
                        if  isinstance(vars, variables):
                            vars_inc[key]      = vars
                            data_vars_inc[key] = instance.data_db[key][cls.KEY_VARS].query(f"group=='{vars.group}'")    
                    #
                    if   len(data_vars_inc)>0:
                        instance.vars_inc    = vars_inc
                        instance.vars_inc_db = data_vars_inc
                    else:
                        instance.vars_inc    = {'all db': 'all'}
                        instance.vars_inc_db = None
                    #
                    return instance
                else:
                    raise(KeyError("Manifest file is not in correct format. 'load' key\
                                    is not located"))
            else:
                raise(KeyError(f"Manifest file is not in correct format. '{task}' task\
                                is not located"))      
        else:
            raise(KeyError(f"Manifest file is not in correct format. 'data' stage\
                            is not located"))
    #
    def __load_manifest(self):
        fn_manifest = f"{self.structure.src}{self.FNAME_MANIFEST}.yml"
        if os.path.exists(fn_manifest):
            blocks      = {}
            with open(fn_manifest) as fmanifest:
                for read in yaml.safe_load_all(fmanifest):
                    key         = [*read.keys()][0]
                    blocks[key] = read[key]
            #
            return blocks
        else:
            print(Warning("No configuration file was found\n"))
            return None
            
        #
        return blocks       
    #
    def __load_data_with_manifest(self, dbs_info):
        db_data         = {}
        db_vars_include = {}
        for fname_key, fname_params in dbs_info.items():
            if 'vars_include' in fname_params.keys():
                params       = fname_params.copy()
                vars_include = params.pop('vars_include')
                data         = load_project.load_table(**params)
                vars_include = variables(data, vars_include)
                #
                db_data        [fname_key] = data
                db_vars_include[fname_key] = vars_include
            else:
                data               = load_project.load_table(**fname_params)
                db_data[fname_key] = data
                db_vars_include[fname_key] = 'all'
        return db_data, db_vars_include



class variables():
    # TODO: to uppercase
    query_ft_num = {'dtype': 'numeric' , 'type': 'feature'  }
    query_ft_cat = {'dtype': 'category', 'type': 'feature'  }
    query_tg_num = {'dtype': 'numeric' , 'type': 'target'   }
    query_tg_cat = {'dtype': 'category', 'type': 'target'   }
    query_tm_cat = {'dtype': 'category', 'type': 'treatment'}
    #
    KEY        = 'key'
    FEATURES   = 'feature'
    VARIABLES  = 'variable'
    TARGETS    = 'target'
    TREATMENTS = 'treatment'
    CLUSTERS   = 'cluster'
    USELESS    = 'useless'
    #
    KEY_VARS     = 'variables'
    KEY_VARS_TMP = 'ffeatureeatures'
    #
    def __init__(self, db, group):
        if variables.KEY_VARS in db.keys():
            self.vars_db = db[variables.KEY_VARS].query(f"group=='{group}'")
        elif variables.KEY_VARS_TMP in db.keys():
            print(DeprecationWarning(f"'{variables.KEY_VARS_TMP}' is deprecated, use 'variable' as the data sheet name\n"))
            self.vars_db = db[variables.KEY_VARS_TMP].query(f"group=='{group}'")
        else:
            raise(KeyError("No variable database was passed"))
        #
        self.group   = group
        #
        self.__get_var_types()
    #
    def update_colnames(self, cols):
        #cols -> dict {old_name:new_name}
        for key, values in cols.items():
            tmp = [values]
            if key in self.keys:
                self.keys.remove(key)
                self.keys = self.keys + tmp
            elif key in self.features:
                self.features.remove(key)
                self.features = self.features + tmp
            elif key in self.targets:
                self.targets.remove(key)
                self.targets = self.targets + tmp
            elif key in self.treatments:
                self.treatments.remove(key)
                self.treatments = self.treatments + tmp
            else:
                raise ValueError('Not defined column error')
            #    
            self.all = self.keys + self.features + self.targets + self.treatments
    #
    def drop_colnames(self, cols):
        for col in cols:
            if col in self.keys:
                self.keys.remove(col)
            elif col in self.features:
                self.features.remove(col)
            elif col in self.targets:
                self.targets.remove(col)
            elif col in self.treatments:
                self.treatments.remove(col)
            else:
                raise ValueError('Not defined column error')
            #
            self.all = self.keys + self.features + self.targets + self.treatments
    #
    def __get_var_types(self):
        #
        self.keys       = self.vars_db.query(f"type=='{self.KEY}'"        )[self.VARIABLES].to_list()
        self.features   = self.vars_db.query(f"type=='{self.FEATURES}'"   )[self.VARIABLES].to_list()
        self.targets    = self.vars_db.query(f"type=='{self.TARGETS}'"    )[self.VARIABLES].to_list()
        self.treatments = self.vars_db.query(f"type=='{self.TREATMENTS}'" )[self.VARIABLES].to_list()
        self.useless    = self.vars_db.query(f"type=='{self.USELESS}'"    )[self.VARIABLES].to_list()
        #
        self.all = self.keys + self.features + self.targets + self.treatments
        #
        if self.vars_db[self.CLUSTERS].isnull().all():
            self.clusters = 'Column clusters empty'
        else:
            self.clusters = list(self.vars_db[self.CLUSTERS].unique())
    #
    
    def __get_var_dtype(self, feature):
        DeprecationWarning("Se eliminará")
        query = self.vars_db[self.vars_db.feature==feature]
        return query[['dtype', 'dsubtype']].to_dict('records')[0]
    #
    def get_var_info(self, var_name, level='basic'):
        query = self.vars_db[self.vars_db.feature==var_name]
        if level=='basic':
            var_info = query[['feature', 'type', 'dtype', 'dsubtype', 'reference']].to_dict('records')[0]
        else:
            var_info = query.to_dict('records')[0]
        return var_info
    #
    def query_vars(self, query):
        if isinstance(query, dict):
            df = self.__and_query__(self.vars_db, query)
        elif isinstance(query, list):
            df = self.__repited_key_query__(self.vars_db, query)
        else:
            raise ValueError("Only list and dictionary are accepted as parameters")
        #
        return df.feature.to_list()
    #
    def get_full_group_variables(self):
        def and_query_wrapper(group):
            key       = group[0]
            df_inner  = group[1]
            df_qry    = self.__and_query__( df_inner, dict(zip(keys, key)) )
            
            if key[1] in ['numeric']:
                return key, df_qry['feature'].to_list()
            elif key[1] in ['category']:
                return key, df_qry[['feature', 'reference']].to_dict('records')
            else:
                raise ValueError("Description variable database has undefined tags.\nOnly numeric, category are allowed. date is not implemented, yet.")                
        #
        df     = self.vars_db.query("type!='useless'")
        keys   = ('type', 'dtype', 'dsubtype')
        groups = df.groupby(list(keys))
        
        vars_grouped = list(map(and_query_wrapper, groups))
        vars_grouped = {grp[0]:grp[1] for grp in vars_grouped}
        return vars_grouped
    #
    def __and_query__(self, df, query):
        query = [f"{k}=='{f}'" for k, f in query.items()]
        query = ' & '.join(query)
        query = df.query(query)
        #
        return query
        #
    # REVIEW: 
    def __repited_key_query__(self, df, query):
        query = [[[*f.keys()][0], [*f.values()][0]] for f in query]
        query = pd.DataFrame(query)
        query.columns = 'keys', 'values'
        #
        query_str = []
        for key in query['keys'].unique():
            split = query.query(f"keys=='{key}'")
            split = split.to_dict('records')
            if len(split)<2:
                s = [*split[0].values()]
                query_str.append(f"{s[0]}=='{s[1]}'")
            else:
                unwrap = [f"{s['keys']}=='{s['values']}'" for s in split]
                unwrap = f"({' | '.join(unwrap)})"
                query_str.append(unwrap)
                #
                query_str = ' & '.join(query_str)
        #
        return df.query(query_str)




#NOTE: Deprecated section
####################################################################
def load_table(name, ext, path="./", sheets='none'):
    print(DeprecationWarning(f"{load_table.__name__} se deja solo por compatibilidad, en futuras versiones se eliminara esta función"))
    fname = "{}{}.{}".format(path,name,ext)
    if ext in ['ods', 'xls', 'xlsx']:
        if sheets == 'none':
            sheets = None 
        else:
            sheets = list(sheets)
        #
        data = pd.read_excel(fname,sheet_name=sheets)
    elif ext == 'csv':
        data = pd.read_csv(fname, low_memory=False)
    #
    elif ext == 'sav':
        data = pd.read_spss(fname)
    #
    elif ext in ['ftr', 'fea']:
        data = pd.read_feather(fname)
    #
    else:
        data = None
    #
    return data
#
class __load_context_config__():
    def __init__(self, path, fname_config='config'):
        print(DeprecationWarning(f"{self.__class__} se deja solo por compatibilidad, en futuras versiones se eliminara"))
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
#
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