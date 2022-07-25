import pandas as pd
import pdb

class Export_DF():
    def __init__(self, index=False):
        self.index = index
    #
    def __to_excel(self, dfs: dict, path: str, fname: str, ext: str='xlsx'):
        file = f"{path}{fname}.{ext}"
        #
        with pd.ExcelWriter(file, engine='xlsxwriter') as writer:
            #
            if   isinstance(dfs, pd.DataFrame):
                dfs.to_excel(writer, sheet_name='data', index=self.index)
                #
                writer.save()
                #writer.close()
            elif isinstance(dfs, list):
                try:
                    for n, df in enumerate(dfs):
                        df.to_excel(writer,  sheet_name=f'sheet {n:02d}', index=self.index)
                    #
                except AttributeError as error:
                    print(error)
                    print("\nItems within list are not DataFrame objects")
                    print("Empty document had been stored\n")
                else:
                    writer.save()
                    writer.close()
            elif isinstance(dfs, dict):
                try:
                    for key, df in dfs.items():
                        df.to_excel(writer,  sheet_name=key, index=self.index)
                    #
                except AttributeError as error:
                    print(error)
                    print("\nItems within dict are not DataFrame objects")
                    print("Empty document had been stored\n")
                else:
                    writer.save()
                    writer.close()
            #
            else:
                raise TypeError("Parameter must be a DataFrame or dict {'sheet_names': DataFrames} or a list of DataFrames")
    #
    def __call__(self, data: dict, path: str, fname: str, ext: str):
        if ext in ('xlsx', 'xls'):
            self.__to_excel(data, path, fname, ext)
        else:
            print('Only xlsx extension are supported for the moment')


##DEPRECATED

#DeprecationWarning
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