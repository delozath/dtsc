import pdb

import numpy as np

class FeatureTypes():
    """docstring for ."""

    def __init__(self,db):
        self.KEY        = 'key'
        self.FEATURES   = 'feature'
        self.TARTETS    = 'target'
        self.TREATMENTS = 'treatment'
        self.ALL        = 'all'
        
        self.db         = db
    
    def update_colnames(self,cols):
        for key,values in cols.items():
            tmp = list(values)
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
                raise ValueError ('Not defined column error')
            
            self.all = self.keys + self.features + self.targets + self.treatments
    
    def drop_colnames(self,cols):
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
                raise ValueError ('Not defined column error')
            
            self.all = self.keys + self.features + self.targets + self.treatments
    
    def query_df_columns(self,group,table='features'):
        query                  = self.db[table].query("group=='%s'"%group)
        """
        types                  = {}
        types[self.KEY       ] = query[query['type']==self.KEY       ]['feature'].to_list()
        types[self.FEATURES  ] = query[query['type']==self.FEATURES  ]['feature'].to_list()
        types[self.TARTETS   ] = query[query['type']==self.TARTETS   ]['feature'].to_list()
        types[self.TREATMENTS] = query[query['type']==self.TREATMENTS]['feature'].to_list()
        """
        self.keys       = query[query['type']==self.KEY       ]['feature'].to_list()
        self.features   = query[query['type']==self.FEATURES  ]['feature'].to_list()
        self.targets    = query[query['type']==self.TARTETS   ]['feature'].to_list()
        self.treatments = query[query['type']==self.TREATMENTS]['feature'].to_list()
        self.all        = self.keys + self.features + self.targets + self.treatments