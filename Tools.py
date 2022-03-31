import re

import numpy  as np
import pandas as pd

import pdb

def statsmodels_col_names(df, cols):
    rep = lambda l, lib: [lib.sub("[/\s()]", '_', c) for c in l]
    
    if isinstance(cols, pd.core.indexes.base.Index):
        vars       = list(cols)
        new_cnames = rep(vars, re)
        new_cnames = dict(zip(vars, new_cnames))
    
    # explicit test the case when class is an dtsc.features.cvars objects
    else:
        vars = []
        for i in ['features', 'keys', 'targets', 'treatments']:
            vars += getattr(cols, i)
        
        new_cnames = rep(vars, re)
        new_cnames = dict(zip(vars, new_cnames))
        
        cols.update_colnames(new_cnames)
    
    return df.rename(columns=new_cnames)

def get_col_types(df, ft, tg):
    
    if len(ft)<2:
        raise IndexError("The number of features must be at least 2")
    
    ft_cat = df[ft].select_dtypes(exclude=np.number).columns.values
    ft_num = df[ft].select_dtypes(include=np.number).columns.values
    
    col_types = {}
    #TODO: verificar para categoricos y fechas
    if df[tg].dtype==np.number:
        col_types['tg'] = {tg:'num'}
    else:
        col_types['tg'] = {tg:'cat'}
    
    col_types['ft'] = { 'cat':ft_cat,
                        'num':ft_num  }
    return col_types

def get_formula_patsy(col_types):
    #TODO: agregar referencia de treatment
    formula  = ' + '.join(col_types['ft']['cat'])
    formula += ' + '.join(col_types['ft']['num'])
    
    target  = [*col_types['tg'].keys()][0]
    #TODO: verificar para categoricos y fechas
    if [*col_types['tg'].values()][0]=='num':
        target  = [*col_types['tg'].keys()][0]
        formula = f"{target} ~ {formula}"
    else:
        formula = f"C({target}) ~ {formula}"
    
    return formula

class RandomTunningValidationSplit():
    """docstring for CrossValidation."""
    from numpy        import arange
    from numpy.random import shuffle
    
    def __init__(self, X, Y, p=0.7):
        self.SAMPLES     = 0
        self.NTRAIN      = 0
        self.NVALIDATION = 1
        
        self.X     = X
        self.Y     = Y
        self.shape = X.shape
        self.p     = p
        
        self.nsamples = self._get_nsamples()
    
    def _get_nsamples(self):
        n_train      = int(self.shape[self.SAMPLES]*self.p)
        n_validation = self    .shape[self.SAMPLES]-n_train
        return n_train,n_validation
    
    def split(self):
        index = self.arange(self.shape[self.SAMPLES])
        self.shuffle(index)
        
        self.X_Tunning = self.X[:self.nsamples[self.NTRAIN]]
        self.Y_Tunning = self.Y[:self.nsamples[self.NTRAIN]]
        
        self.X_Validation = self.X[-self.nsamples[self.NVALIDATION]:]
        self.Y_Validation = self.Y[-self.nsamples[self.NVALIDATION]:]

from time import localtime, strftime

def seed():
    t  = localtime()
    ct = strftime("%-S%-d%-H%-M", t)
    return int(ct)

def file_name(prefix, GROUP, TREATMENT, TARGET, extension=""):
    fname = '{} FTG-{} TRM-{} TGT-{}'.format(prefix, GROUP, TREATMENT, TARGET)
    if extension!="":
        fname += '.{}'.format(extension)
    
    return fname

def random_p_split( N:int=100, p:float=0.7)->dict:
    """
    Generates random-shuffled indexes
         
    Parameters:
    ----------
    N : int
        list lenght
    p : float
        proportion of split
    
    Returns:
    -------
      index : dict
          S0 : firsts int(N*p) elements of random-shuffled index
          S1 : Last int(N*(1-p)) elements of random-shuffled index
    """
    #TODO: to module
    from numpy        import arange
    from numpy.random import shuffle
    
    n_train      = int(N*p)
    n_validation = n_train - N
    
    index = arange(N)
    shuffle(index)
    
    index = {'S0':index[:n_train],'S1':index[n_validation:]}
    return index
    