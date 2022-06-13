import pdb
import yaml

import numpy  as np
import pandas as pd

import seaborn as sns
from matplotlib import pyplot as plt

N_UNIQUE = 6

def basic(data, opath, ext='png'):
    #pdb.set_trace()
    path_img = opath['path'] + opath['subpath']['images']
    path_dat = opath['path'] + opath['subpath']['data']
    
    info = {}
    for var in data.columns:
        print(f"Processing {var}-->")
        series   = data[var]
        #
        if len(series.shape)>1:
            print("----> Columna duplicada, no agregada en exploración\n")
        else:
            unique   = series.unique()
            n_unique = unique.shape[0]
            n_nulls  = series.isnull().sum()
            #
            sns.set(font_scale=1.5)
            if n_unique>N_UNIQUE:
                #
                if series.dtypes==np.int:
                    info[var] = {'type':'numeric', 'subtype': 'int'  , 'nulls': int(n_nulls)}
                else:
                    info[var] = {'type':'numeric', 'subtype': 'float', 'nulls': int(n_nulls)}
                #
                g = sns.displot(x=var, data=data, height=12, aspect=12/8)
            else:
                #test numeric data
                if np.issubdtype(series.dtypes, np.number):
                    if series.dtypes==np.int:
                        tmp = {'type': 'category', 'subtype': 'int', 'nulls': int(n_nulls)}
                    else:
                        tmp = {'type': 'category', 'subtype': 'float', 'nulls': int(n_nulls)}
                else:
                    tmp = {'type': 'category', 'subtype': 'object', 'nulls': int(n_nulls)}
                    #tmp['value_counts'] = series.value_counts().to_dict()
                tmp['value_counts'] = str(series.value_counts().to_dict())[1:-1]
                #
                info[var] = tmp
                #
                plt.figure(figsize=(12,8))
                g = sns.countplot(x=var, data=pd.DataFrame(series.fillna('Missing')))
                g.bar_label(g.containers[0], fontsize=15)
            #
            plt.tight_layout()
            g.figure.savefig(f"{path_img}{var}.{ext}")
            g.figure.clear()
            plt.close()
            #
    df         = pd.DataFrame(info).T.reset_index()
    df.columns = ['variable'] + df.columns.to_list()[1:]
    fname      = f"{path_dat}{opath['name']}.{opath['ext']}"
    df.to_csv(fname, index=False)
    
    #DeprecationWarning para bases de datos pequeñas es más facil con
    #una base de datos relacional en lugar de un yaml
    """
    with open(fname, 'w+') as f:
        yaml.dump({'Column Exploration': info}, f, allow_unicode=True)
    """
    #
    print(f"\nExplore figures stored in \n{path_img}...\n\n")
    pdb.set_trace()

def cat_numeric_uniques(df, cols, ft_types, sep=','):
    query    = ' | '.join([f"var=='{i}'" for i in cols])
    ft_cat   = ft_types.query(f"({query}) & (type=='category')")
    ft_cat   = ft_cat['var'].to_list()
    #
    df_num_cat             = df[ft_cat].select_dtypes(include=np.int).astype('int')
    df[df_num_cat.columns] = df_num_cat
    
    col_names = df.columns.to_list()
    uniques   = df[df_num_cat.columns].dropna().astype('str').apply(f'{sep}'.join, axis=1).unique()
    #
    df['cat_code'] = -1
    #
    codes   = []
    for n,u in enumerate(uniques):
        code  = [int(i) for i in u.split(sep)]
        query = [f"{i}=={j}" for i,j in zip(df_num_cat.columns, code)]
        query = ' & '.join(query)
        index = df.query(query).index
        #
        df.loc[index, 'cat_code'] = n
        #
        codes.append(code + [n] + list(index.shape))
    #codes = np.array(codes)
    codes = pd.DataFrame(codes, columns=df_num_cat.columns.to_list() + ['cat_code', 'n_in_cat_code'])
    codes = codes.sort_values('n_in_cat_code', ascending=False)
    #
    return df, codes

#TODO:

def __representation__(val, ft, type):
    if val=='nan':
        return f"{ft}.isnull()"
    if type=='float':
        return f"{ft}=={val}"
    elif type=='int':
        return f"{ft}=={val}"
    else:
        return f"{ft}=='{val}'"

def cat_combination_analysis(df, features, vars_info, sep=';'):
    codes      = []
    categories = {}
    for ft in features:
        if vars_info[ft]['type']=='category':
            categories[ft] = vars_info[ft]['subtype']
    #
    uniques = df[categories.keys()].astype('str').apply(sep.join, axis=1).unique()
    for n,u in enumerate(uniques):
        print(f"Processing Grupo: {n+1} de {len(uniques)}")
        rep   = map(__representation__, u.split(sep), categories.keys(), categories.values())
        query = ' & '.join(list(rep))
        #
        codes.append({'grupo': n, 'cuenta': df.query(query).shape[0]})
    return pd.DataFrame(codes)
