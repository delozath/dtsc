import numpy   as np
import pandas  as pd
import seaborn as sns

from matplotlib import pyplot as plt

import pdb

def cluster_add(df, labels, index=""):
    clusters       = pd.Series(labels)
    clusters.name  = 'cluster'
    if index=="":
        X = pd.concat((df.reset_index(),clusters), axis=1).set_index('index')
    else:
        X = pd.concat((df.reset_index(),clusters), axis=1).set_index(index)
    
    X['cluster']      = X['cluster'].astype('category')
    uniques,  n_elems = np.unique(labels, return_counts=True)
    return X.copy(), uniques, n_elems