import pdb


class cvars():
    """docstring for ."""
    #
    def __init__(self, db, group):
        self.KEY        = 'key'
        self.FEATURES   = 'feature'
        self.TARGETS    = 'target'
        self.TREATMENTS = 'treatment'
        self.CLUSTERS   = 'cluster'
        self.USELESS    = 'useless'
        #
        self.vars_db = db['features'].query(f"group=='{group}'")
        self.group   = group
        #
        self.__get_var_types__()
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
    def __get_var_types__(self):
        #
        self.keys       = self.vars_db.query(f"type=='{self.KEY}'"        )[self.FEATURES].to_list()
        self.features   = self.vars_db.query(f"type=='{self.FEATURES}'"   )[self.FEATURES].to_list()
        self.targets    = self.vars_db.query(f"type=='{self.TARGETS}'"    )[self.FEATURES].to_list()
        self.treatments = self.vars_db.query(f"type=='{self.TREATMENTS}'" )[self.FEATURES].to_list()
        self.useless    = self.vars_db.query(f"type=='{self.USELESS}'"    )[self.FEATURES].to_list()
        #
        self.all = self.keys + self.features + self.targets + self.treatments
        #
        if self.vars_db[self.CLUSTERS].isnull().all():
            self.clusters = 'Column clusters empty'
        else:
            self.clusters = list(self.vars_db[self.CLUSTERS].unique())
    #    
    #TODO parametro para especificar que tipo de variable se modificaraf
    #en esta version se quitan todos los espacios de todas las columnas
    def drop_spaces_cnames(self, crep='_'):
        pdb.set_trace()
    #
    def get_var_dtype(self, feature):
        query = self.vars_db[self.vars_db.feature==feature]
        return query[['dtype', 'dsubtype']].to_dict('records')[0]
    
    def get_var_dtypes(self):
        dtypes = {}
        for key, df in self.vars_db.groupby(['type', 'dtype', 'dsubtype']):
            if  not('useless' in key):
                dtypes[key] = list(df.feature.values)
        #
        return dtypes