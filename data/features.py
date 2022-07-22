import pdb

import pandas as pd

class cvars():
    query_ft_num = {'dtype': 'numeric' , 'type': 'feature'  }
    query_ft_cat = {'dtype': 'category', 'type': 'feature'  }
    query_tg_num = {'dtype': 'numeric' , 'type': 'target'   }
    query_tg_cat = {'dtype': 'category', 'type': 'target'   }
    query_tm_cat = {'dtype': 'category', 'type': 'treatment'}
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
