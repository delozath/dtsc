import pdb


class cvars():
    """docstring for ."""
    #
    def __init__(self, db, group):
        self.KEY        = 'key'
        self.FEATURES   = 'feature'
        self.TARTETS    = 'target'
        self.TREATMENTS = 'treatment'
        self.CLUSTERS   = 'cluster'
        self.ALL        = 'all'
        self.USELESS    = 'useless'
        self.table      = 'features'
        #
        self.db    = db
        self.group = group
        #
        self._query_df_columns()
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

    def _query_df_columns(self):
        query = self.db[self.table].query("group=='%s'" % self.group)
        #
        self.keys = query[query['type'] == self.KEY][self.FEATURES].to_list()
        self.features = query[query['type']
                              == self.FEATURES][self.FEATURES].to_list()
        self.targets = query[query['type']
                             == self.TARTETS][self.FEATURES].to_list()
        self.treatments = query[query['type']
                                == self.TREATMENTS][self.FEATURES].to_list()
        self.useless = query[query['type']
                             == self.USELESS][self.FEATURES].to_list()
        self.all = self.keys + self.features + self.targets + self.treatments
        #
        #cluster de variables
        #TODO try-except cuando no hay columna cluster
        df = query[query['type'] != 'useless']
        clusters = {i: j['feature'].to_list()
                    for i, j in df.groupby('cluster')}
        self.clusters = clusters
    #    
    #TODO parametro para especificar que tipo de variable se modificara
    #en esta version se quitan todos los espacios de todas las columnas
    def drop_spaces_cnames(self, crep='_'):
        pdb.set_trace()
