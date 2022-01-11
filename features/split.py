
#import numpy  as np
import pandas as pd

from numpy import linspace, array, arange
from numpy.random import shuffle

import pdb



class Quantile_Splits():
    """docstring for ."""
    def __init__(self):
        pass
    
    def __blocks_q__(self, y, nb):
        #TODO generalizar para np.array
        lims   = linspace(0, 1, nb)
        blocks = {}
        for n, (low,high) in enumerate( zip(lims[:-2], lims[1:-1]) ):
            bl, bh                = y.quantile(low), y.quantile(high)
            blocks[f'Q{high:0.2f}'] =  (y>=bl) & (y<bh)
        
        blocks[f'Q{lims[-1]:0.2f}'] = (y>=bh)
        
        return blocks
    
    def __block_split__(self, y, mask, porc):
        self.split = {}
        #TODO: case para diferentes parametros, lista por ejemplo
        if isinstance(porc, float):
            for bk, mk in mask.items():
                l   = y[mk].shape[0]
                n   = int(l*porc)
                sel = arange(l)<n
                shuffle(sel)
                
                self.split[f"{bk}"] = {'train':y.index[mk][sel], 'test':y.index[mk][~sel]}
    
    def flatten_blocks(self):
        train, test = [], []
        for _, val in self.split.items():
            train += list(val['train']) 
            test  += list(val['test' ])
        
        return train, test
    
    #TODO: actualizar esto
    def tmp_store_splits(self,splits):
        index = lambda ix: ';'.join([str(i) for i in ix])
        df_idx = pd.DataFrame()
        for id, split in splits.items():
            for ft, idx in split.items():
                df_idx = df_idx.append(\
                             {'id':id, 
                              'ft':ft,
                              'idx_tn':index(idx['idx_train']),
                              'idx_tt':index(idx['idx_test' ])},
                             ignore_index=True)
        return df_idx
    
    def reg_qsplit(self, y, nb=4, porc=0.7):
        masks = self.__blocks_q__(y, nb+1)
        self.__block_split__(y, masks, porc)
        