import pandas as pd
import pdb

class save_dataframe():
    """docstring for save."""

    def __init__(self, cfg_save: dict, index=False):
        self.cfg_save = cfg_save
        self.index    = index
    
    def data_frames_to_datasheets(self, dfs, fname='DataFrame'):
        if not isinstance(dfs, (tuple, list)):
            dfs = [dfs]
        #
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
        #
        writer.save()
        writer.close()


class export_dataframe(save_dataframe):
    def __init__(self, cfg_save: dict, index=False):
        super().__init__(cfg_save, index)
    
    def init_feature_sheet(self, df):
        features = {'feature'  : df.columns.to_list(),
                    'data type': df.dtypes.values,
                    'info'     : [str(i.type) for i in df.dtypes]}
        
        features = pd.DataFrame(features)
        features['group']   = 'init'  
        features['type']    = 'useless'
        features['cluster'] = ''
        
        features = features[['group',
                             'feature',
                             'type',
                             'cluster',
                             'data type',
                             'info']]
        #
        return features
    
    def export(self, dfs, fname=''):
        if fname=='':
            path  = self.cfg_save['path']
            name  = self.cfg_save['name']
            ext   = self.cfg_save['ext']
            fname = f"{path}{name}.{ext}"
        #
        if self.cfg_save['ext'] in ['ods', 'xlsx', 'xlsx']:
            self.data_frames_to_datasheets(dfs, fname=fname)

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