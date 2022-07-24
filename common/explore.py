import pdb
import yaml
import pyperclip

import numpy  as np
import pandas as pd

import seaborn as sns
from matplotlib import pyplot as plt

import statsmodels.api as sm

from itertools import combinations

from dtsc.data.save import Export_DF

N_UNIQUE = 6
KEY_VARS = 'variable'
#TODO complete join analysis to main database
def initial(data, paths, vars_inc_db='', fname='exploration', ext='png'):
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
                    info[var] = {'dtype':'numeric', 'subtype': 'int'  , 'nulls': int(n_nulls)}
                else:
                    info[var] = {'dtype':'numeric', 'subtype': 'float', 'nulls': int(n_nulls)}
                #
                g = sns.displot(x=var, data=data, height=12, aspect=12/8)
            else:
                #test numeric data
                if np.issubdtype(series.dtypes, np.number):
                    if series.dtypes==np.int:
                        tmp = {'dtype': 'category', 'subtype': 'int', 'nulls': int(n_nulls)}
                    else:
                        tmp = {'dtype': 'category', 'subtype': 'float', 'nulls': int(n_nulls)}
                else:
                    tmp = {'dtype': 'category', 'subtype': 'object', 'nulls': int(n_nulls)}
                    #tmp['value_counts'] = series.value_counts().to_dict()
                tmp['value_counts'] = str(series.value_counts().to_dict())[1:-1].replace(',', ';')
                #
                info[var] = tmp
                #
                plt.figure(figsize=(12,8))
                g = sns.countplot(x=var, data=pd.DataFrame(series.fillna('Missing')))
                g.bar_label(g.containers[0], fontsize=15)
            #
            plt.tight_layout()
            g.figure.savefig(f"{paths.images}{var}.{ext}")
            g.figure.clear()
            plt.close()
            #
    df         = pd.DataFrame(info).T.reset_index()
    df.columns = [KEY_VARS] + df.columns.to_list()[1:]
    #
    if isinstance(vars_inc_db, str):
        pyperclip.copy(df.to_csv(index=False))
        msg = 'Data type analysis copied to clipboard'
        input(f"\n\nLOG_INFO: {msg}, press any to continue...\n\n")
    #TODO test for especific class
    elif isinstance(vars_inc_db, pd.DataFrame):
        df = df.set_index(KEY_VARS)
        df = df.join(vars_inc_db.set_index(KEY_VARS),  rsuffix='_join').reset_index()
        #
        export = Export_DF()
        
        export(df, paths.data, 'test', 'xlsx', )
        pdb.set_trace()
    #
    else:
        raise TypeError("Only string or DataFrame admitted")

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
    
def pair_numeric_corr(df, cols):
    corr_map = pd.DataFrame()
    for x_0, x_1 in combinations(cols, 2):
        X    = df[[x_0, x_1]]
        corr = np.corrcoef(X[x_0], X[x_1])[0,1]
        print(f"""{corr:5.3f}\n   - {x_0}\n   - {x_1}\n""")
        tmp      = pd.DataFrame({'x_0': x_0, 'x_1': x_1, 'corr': corr}, index=[1])
        corr_map = pd.concat((corr_map, tmp), axis=0)
    #
    sns.set(font_scale=.8)
    ax = plt.axes()
    g  = sns.heatmap( corr_map.pivot('x_0', 'x_1', 'corr'),
           annot=True, fmt="5.3f", linewidths=.5, cmap='PiYG',
           vmin=-1, vmax=1, ax=ax )
    plt.tight_layout()
    #g.figure.show()
    plt.show()

def pair_category_corr(df, cols):
    pvalues = pd.DataFrame()
    for x_0, x_1 in combinations(cols, 2):
        X      = df[[x_0, x_1]]
        table  = sm.stats.Table.from_data(X)
        pvalue = table.test_nominal_association().pvalue
        print(f"""{pvalue}\n   - {x_0}\n   - {x_1}\n""")
        tmp     = pd.DataFrame({'x_0': x_0, 'x_1': x_1, 'pvalue': pvalue}, index=[1])
        pvalues = pd.concat((pvalues, tmp), axis=0)
    #
    sns.set(font_scale=.8)
    ax = plt.axes()
    g  = sns.heatmap( pvalues.pivot('x_0', 'x_1', 'pvalue'),
           annot=True, fmt="5.3f", linewidths=.5, cmap='YlGnBu',
           vmin=0, vmax=1, ax=ax )
    plt.tight_layout()
    #g.figure.show()
    plt.show()
       