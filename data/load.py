import pandas as pd
import pdb

def table(name,ext,path="./"):
    fname = "{}{}.{}".format(path,name,ext)
    if ext == 'ods' or ext == 'xls' or ext == 'xlsx':
        if file['sheets'] == 'none':
            sheets = None 
        else:
            sheets = list(file['sheets'])
        
        data = pd.read_excel(fname,sheet_name=sheets)
    elif ext == 'csv':
        data = pd.read_csv(fname)
    else:
        data = -1
    
    return data