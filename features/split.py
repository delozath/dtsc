
#import numpy  as np
import pandas as pd

from numpy import linspace, array
from numpy.random import shuffle

import pdb



class Quantile_Splits():
    """docstring for ."""
    def __init__(self):
        pass
    
    def __get_interval_index__(self, target, limits):
        limits = array(limits)
        mask   = {'block0':(target<limits[0]).to_numpy()}
        for n, (low, high) in enumerate( zip(limits[:-1],limits[1:]) ):
            mask[f'block{n+1}'] = ((target>=low) & (target<high)).to_numpy()
        
        mask[f'block{n+2}'] = (target>=limits[-1]).to_numpy()
        
        return mask
    
    def __get_q_blocks_nbins__(self, target, nbins):
        limits  = linspace(0, 1, nbins)
        qs_lims = []
        for lim in limits[1:-1]:
            qs_lims.append(target.quantile(lim))
        
        return qs_lims
    
    def __get__split__(self, df, blocks, porc_train):
        train, test = [], []
        
        for block, mask in blocks.items():
            print(f"Procesando {block}")
            index = df[mask].index.values
            N     = int(index.shape[0]*porc_train)
            shuffle(index)
            
            train += list(index[:N])
            test  += list(index[N:])
        
        
        pdb.set_trace()
    
    def reg_q_split(self, df_targets, nbins=5, porc_train=0.7):
        if isinstance(nbins, int):
            #mask    = {}
            for target in df_targets.columns:
                df      = df_targets[target]
                qs_lims = self.__get_q_blocks_nbins__(df, nbins)
                mask    = self.__get_interval_index__(df, qs_lims)
                self.__get__split__(df,mask,porc_train)
            #self.__get_interval_index__(df_targets['MGkg'], df['MGkg'])
            pdb.set_trace()
        