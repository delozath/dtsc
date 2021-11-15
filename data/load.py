import pandas as pd


def table(name,ext,path="./",sheets='none'):
    fname = "{}{}.{}".format(path,name,ext)
    #if ext == 'ods' or ext == 'xls' or ext == 'xlsx':
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