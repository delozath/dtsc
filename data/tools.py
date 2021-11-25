#model is a Statsmodels GLM or logistic regression model
def statsmodels_odd_ratios(model):
    params             = model.params
    conf               = model.conf_int()
    conf['Odds Ratio'] = params
    conf.columns       = ['5%', '95%', 'Odds Ratio']
    conf               = conf[['Odds Ratio', '5%', '95%']]
    return conf