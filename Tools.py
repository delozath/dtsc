import pdb

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

class Arguments():
    """docstring for ."""
    import argparse

    def __init__(self,prog,descr):
        self.prog  = prog
        self.descr = descr
    
    #TODO hacerlo una clase abstracta para generalizar los posibles argumentos
    def get_args(self,type):
        parser = self.argparse.ArgumentParser( prog=self.prog, description=self.descr)
        
        if type=='group-treatment-targets':
            parser.add_argument( '--group'    ,
                                 '-g'          ,
                                 action='store',
                                 nargs='?'     ,
                                 default='raw' )
            parser.add_argument('--treatment'  ,
                                 '-t'          ,
                                 action='store',
                                 nargs='?'     ,
                                 default='X' )
            parser.add_argument('--targets'  ,
                                 '-r'          ,
                                 action='store',
                                 nargs='+'     ,
                                 default=['X'] )
        else:
            parser.add_argument( 'None'    ,
                                 action='store',
                                 nargs='?'     ,
                                 default='none' )            
        
        return parser.parse_args()
        

class ImportData():
    """docstring for ImportData. """
    import time
    import pathlib
    
    import pandas as pd
    
    def __init__(self, sname, PREFIX='DBAE', PATH='/store/science/data/'):
        self.path      = PATH
        year           = self.time.strftime("%Y")
        self.fdata     = '{} DB {} {}'  .format( PREFIX,
                                                 year  ,
                                                 sname )
        self.finfo     = '{} INFO {} {}'.format( PREFIX,
                                                 year  ,
                                                 sname )
        self.__ext     = -3
    
    def _spss2csv(self,fname):
        data = self.pd.read_spss(fname)
        col, typ, cat = [], [], []
        for d,t in zip(data.columns,data.dtypes):
            cats = 'numeric'
            if t.name=='category':
                cats = '; '.join([str(i) for i in t.categories])
            elif t.name=='object':
                cats = 'string'
            #print(d,t.name,cats)
            col.append(d)
            typ.append(t.name)
            cat.append(cats)
        
        df = self.pd.DataFrame.from_dict({'group':'raw','feature':col,'type':'','data type':typ,'categories':cat,'info':''})
        df  .to_csv(self.path+self.finfo+'.csv',index=False)
        data.to_csv(self.path+self.fdata+'.csv',index=False)
        
        print('\n\nImported data to:\n\t', 
               self.path+self.finfo+'.csv', '\n\t', 
               self.path+self.fdata+'.csv','\n\n')
    
    def __file_exist(self,fname):
        return self.pathlib.Path(fname).is_file()
    
    #TODO try-catch statements
    def load(self,fname):
        if self.__file_exist(fname):
            if fname[self.__ext:] == 'sav':
                self._spss2csv(fname)
            else:
                print("\n\nNo decoder available\n\n")
        else:
            print("\n\nFile not exist\n\n")

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
    