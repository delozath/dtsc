import pandas as pd
import pdb

from dtsc.data.structure import paths

class Save_File():
    """docstring for Save."""

    def __init__(self, cfg_save: dict, index=False):
        self.cfg_save = cfg_save
        self.index    = index
    
    def save(self, dfs: tuple, fname=''):
        if fname=='':
            fname  = f"{self.cfg_save['path']}{self.cfg_save['name']}.{self.cfg_save['ext']}"
        
        #Save Excel-like tables
        if self.cfg_save['ext'] in ['ods', 'xlsx', 'xlsx']:
            writer = pd.ExcelWriter(fname)
            
            if 'sheets' in self.cfg_save.keys():
                if len(self.cfg_save['sheets']) == len(dfs):
                    for df, sheet in zip(dfs, self.cfg_save['sheets']):
                        df.to_excel(writer, sheet, index=self.index)
                #TODO general match sheet that names unknow sheets (not present in config file)
                else:
                    print("TODO: len sheet names and data frame number do not macht")
            else:
                for n, df,  in enumerate(dfs):
                    df.to_excel(writer, f"Sheet {n+1}", index=self.index)                
            
            writer.save()
            writer.close()        
        
        print(f"\n\nData saved corretly in\n{fname}\n\n\n")