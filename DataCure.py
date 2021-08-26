import feather

import pdb

import numpy as np

from sklearn.base import TransformerMixin

class Cure():
    """docstring for ."""
    def __init__(self,df,info,group):
        self.GROUP     = group
        self.TARGET    = 'target'
        self.FEATURE   = 'feature'
        self.TREATMENT = 'treatment'
        self.CATEGORY  = 'category'
        
        self.df   = df
        self.info = info
    
    def query(self,df,query):
        return df.query(query)
        
    def categories(self):
        query    = "group=='%s' & type=='%s'"%(self.GROUP,self.CATEGORY)
        features = self.query(self.info['Features'],query).feature.to_list()
        
        for f in features:
            self.df = self.df.astype({f: 'category'})
            
    def save_feather(self,path):
        feather.write_dataframe(self.df, path)
        
    def dropna(self):
        index_x = self.X_.isnull().sum(axis=1).to_numpy()
        index_y = self.Y_.isnull().sum(axis=1).to_numpy()
        index_t = self.T_.isnull().sum(axis=1).to_numpy()
        
        index_x = set(np.where(index_x==0)[0])
        index_y = set(np.where(index_y==0)[0])
        index_t = set(np.where(index_t==0)[0])
        
        # TODO: manage for no treatment variable
        index      = index_x.intersection(index_y,index_t)
        self.index = np.array(list(index))
    
    def splits(self):
        query    = "group=='%s' & type=='%s'"%(self.GROUP,self.FEATURE)
        features = self.query(self.info['Features'],query).feature.to_list()
        
        query    = "group=='%s' & type=='%s'"%(self.GROUP,self.TARGET)
        targets  = self.query(self.info['Features'],query).feature.to_list()
        
        query      = "group=='%s' & type=='%s'"%(self.GROUP,self.TREATMENT)
        treatments = self.query(self.info['Features'],query).feature.to_list()
        
        #pdb.set_trace()
        self.X_ = self.df[features]
        self.Y_ = self.df[targets]
        self.T_ = self.df[treatments]
        
        self.features   = features
        self.targets    = targets
        self.treatments = treatments

    def fit(self):
        self.splits()
        self.dropna()
        self.X_ = self.X_.iloc[self.index]
        self.Y_ = self.Y_.iloc[self.index]
        self.T_ = self.T_.iloc[self.index]
    
    def set_dtype_filter(self,df,**kwargs):
        newdtype  = kwargs.pop('dtype')
        conds     = df.filter(**kwargs).columns
        df[conds] = df[conds].astype(newdtype)
    
    def get_target_formulas(self):
        query = "group=='%s' & type=='%s'"%(self.GROUP,self.TARGET)
        df    = self.query(self.info['Formulas'],query)[['feature','formula']]
        
        formulas = {i:j for i,j in zip( df.feature.to_list(),
                                        df.formula.to_list() )}
        return formulas
        

class LabelEncoderParser(TransformerMixin):
    from numpy  import array
    from pandas import DataFrame
    from sklearn.preprocessing import LabelEncoder
    def __init__(self, *args, **kwargs):
        self.args    = args
        self.kwargs  = kwargs
        self.encoder = []
    def fit(self, x, y=None):
        data = x
        if isinstance(x, self.DataFrame):
            data = x.to_numpy()
        l = x.shape[-1]
        self.encoder = [self.LabelEncoder(*self.args, **self.kwargs) for i in range(l) ]
        for e,d in zip(self.encoder,data.T):
            e.fit(d)
        return self
    def transform(self, x, y=None):
        data = x
        if isinstance(x, self.DataFrame):
            data = x.to_numpy()
        x_t = [s.transform(d) for s,d in zip(self.encoder,data.T)]
        return self.array(x_t).T.copy()

class DFLabelEncoder():
    from pandas import DataFrame
    def __init__(self,df):
        self.__N_CATEGORIES__ = -1
        self.df = df
    def fit(self,columns=0):
        dfl = []
        if columns!=0:
            dfl = self.DataFrame()
            cat = {}
            for c in columns:
                tmp = self.df[c].cat.codes
                dfl = dfl.assign(**{c:tmp})
                
                tmpcat   = self.df[c].cat.categories.to_list()
                tmpcat  += [len(tmpcat)]
                cat[c]   = tmpcat
            self.categories_ = cat
        else:
            for c in self.df.columns:
                if self.df[c].dtypes.name=='category':
                    tmp      = self.df[c].cat.codes
                    self.df  = self.df.assign(**{c:tmp})
            
        return self.df
    
    def get_ncategories(self,col):
        return self.categories_[col][self.__N_CATEGORIES__]

to_positiveclass = lambda y:  2*y - 1
to_negativeclass = lambda y: -2*y + 1



# deprecated
class EncodeNumeric():
    """docstring forEncoders"""
    
    def __init__(self, df):
        self.df = df
    
    def get_categories(self):
        self.categories = self.df.select_dtypes(include='category').columns.to_list()
    
    def fit(self):
        self.get_categories()
        
        self.codes_       = {}
        self.code_counts_ = {}
        for cat in self.categories:
            category = self.df[cat].cat.categories.to_list()
            self.codes_      [cat] = category
            self.code_counts_[cat] = self.df[cat].value_counts().to_dict()
            
            tmp     = self.df[cat].cat.codes.to_numpy()
            self.df = self.df.assign(**{cat:tmp})
            #self.df[cat] = self.df[cat].cat.codes
