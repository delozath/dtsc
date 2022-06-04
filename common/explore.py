import numpy  as np
import pandas as pd
import pdb

import seaborn as sns
from matplotlib import pyplot as plt

N_UNIQUE = 6

def basic(data, opath, ext='png'):
    df = pd.DataFrame()
    for var in data.columns:
        print(f"Processing {var}-->")
        series   = data[var]
        #
        if len(series.shape)>1:
            print("----> Columna duplicada, no agregada en exploración\n")
        else:
            unique   = series.unique()
            n_unique = unique.shape[0]
            #
            sns.set(font_scale=1.5)
            row = {'var':var}
            if n_unique>N_UNIQUE:
                g = sns.displot(x=var, data=data, height=7, aspect=7/5)
                row['type'] = 'numeric'
            else:
                g = sns.countplot(x=var, data=data)
                g.bar_label(g.containers[0], fontsize=15)
                row['type'] = 'category'
            #
            plt.tight_layout()
            g.figure.savefig(f"{opath}{var}.{ext}")
            g.figure.clear()
            plt.close()
            #
            df = pd.concat((df, pd.DataFrame(row, index=[1])), axis=0)
    print(f"\nExplore figures stored in \n{opath}{var}.{ext}...\n\n")
    return df

def cat_numeric_uniques(df, sep=','):
    cols    = df.columns.to_list()
    uniques = df.dropna().astype('str').apply(f'{sep}'.join, axis=1).unique()
    #
    df['cat_code'] = -1
    #
    codes   = []
    for n,u in enumerate(uniques):
        #pdb.set_trace()
        code  = [int(i) for i in u.split(sep)]
        query = [f"{i}=={j}" for i,j in zip(df.columns, code)]
        query = ' & '.join(query)
        index = df.query(query).index
        #
        df.loc[index, 'cat_code'] = n
        #
        codes.append(code + [n] + list(index.shape))
    #codes = np.array(codes)
    codes = pd.DataFrame(codes, columns=cols + ['cat_code', 'n_in_cat_code'])
    codes = codes.sort_values('n_in_cat_code', ascending=False)
    #
    return df, codes
