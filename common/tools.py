import pdb

from time import localtime, strftime
import re

import numpy as np
import pandas as pd
import dtsc


class for_statsmodels():
    KEY_VARIABLE     = 'variable'
    DROP_CHARS_REGEX = r"[/\s()-]"
    @staticmethod
    def drop_space_colnames(df, vars_inc, vars_inc_db=''):
        def rep(l, lib): return [lib.sub(for_statsmodels.DROP_CHARS_REGEX, '_', c) for c in l]
        #
        if   isinstance(vars_inc, list):
            new_cnames = rep(vars_inc, re)
            new_cnames = dict(zip(colnames, new_cnames))
            #
            return df.rename(columns=new_cnames)
        #
        elif isinstance(vars_inc, dtsc.data.load.variables):
            vars       = vars_inc.all
            new_cnames = rep(vars, re)
            new_cnames = dict(zip(vars, new_cnames))
            #
            vars_inc.update_colnames(new_cnames)
            #
            if isinstance(vars_inc_db, pd.DataFrame):
                vars = vars_inc_db[for_statsmodels.KEY_VARIABLE].\
                             str.replace(for_statsmodels.DROP_CHARS_REGEX, '_', regex=True)
                #
                vars_inc_db[for_statsmodels.KEY_VARIABLE] = vars
            #
            return df.rename(columns=new_cnames), vars_inc, vars_inc_db
        #

def statsmodels_col_names____(df, cols):
    def rep(l, lib): return [lib.sub("[/\s()-]", '_', c) for c in l]
    #
    if isinstance(cols, pd.core.indexes.base.Index):
        vars = list(cols)
        new_cnames = rep(vars, re)
        new_cnames = dict(zip(vars, new_cnames))
    #
    # explicit test the case when class is an dtsc.features.cvars objects
    elif isinstance(cols, dtsc.data.features.cvars):
        vars = []
        for i in ['features', 'keys', 'targets', 'treatments']:
            vars += getattr(cols, i)
        #
        new_cnames = rep(vars, re)
        new_cnames = dict(zip(vars, new_cnames))
        #
        cols.update_colnames(new_cnames)
    else:
        raise TypeError("Not supported class to update column names")
    #
    return df.rename(columns=new_cnames)

def get_patsy_reference(cat_vars):
    def get_references(cat):
        if cat['dsubtype']   in ('int', 'float'):
            return f"C({cat['feature']}, Treatment(reference={cat['reference']}))"
        elif cat['dsubtype'] in ('object', 'category'):
            return f"C({cat['feature']}, Treatment(reference='{cat['reference']}'))"
        else:
            return f"C({cat['feature']})"
    #
    formula = list(map(get_references, cat_vars))
    return ' + '.join(formula)
#
DeprecationWarning()
def __get_patsy_reference(info):
    formula = []
    for k, f in info.items():
        if f['dsubtype'] in ['int', 'float']:
            formula.append(f"C({k}, Treatment(reference={f['reference']}))")
        elif f['dsubtype'] in ['object', 'category']:
            formula.append(f"C({k}, Treatment(reference='{f['reference']}'))")
        else:
            formula.append(f"C({k})")
    return ' + '.join(formula)

def seed():
    t = localtime()
    ct = strftime("%-S%-d%-H%-M", t)
    return int(ct)