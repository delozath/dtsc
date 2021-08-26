import pandas  as pd
import seaborn as sns

from matplotlib import pyplot as plt

import pdb
class ExplorePlots():
    import math
    """docstring forPairPlots."""
    def __init__(self):
        pass
    
    def get_pairs(self):
        cols  = self.features.columns.to_list()
        cols_ = self.features.columns.to_list()
        
        # TODO: lanzar error para numero columnas > 20
        pairs = []
        for c in cols:
            for c_ in cols_:
                pairs.append((c,c_))
            
            del(cols_[0])
        
        return pairs
    
    def pair_plots(self,features,targets):
        self.features = features
        self.targets  = targets
        pairs         = self.get_pairs()
        for pair in pairs:
            if pair[0]!=pair[1]:
                hue = 'ClasifPesoNacer'
                df = pd.concat([self.features.loc[:,pair],self.targets.loc[:,hue]],axis=1)
                df = df.dropna()
                sns.scatterplot(x=pair[0],y=pair[1],hue=hue,data=df,palette='deep',s=100)
                
                df  = df.melt(hue)
                sns.displot(x='value',hue='variable',data=df, kind="kde", fill=True)
                plt.show()
            
        pdb.set_trace()
    
    def _bar_annotate(self,ax,g,values):
        for bar in g.patches:
            barperc = bar.get_height()/sum(values)*100
            barmid  = bar.get_x() + bar.get_width()/2
            g.annotate('{:3.2f}%'.format(barperc)    ,  
                        ( barmid, bar.get_height())  ,
                          ha        ='center'        ,
                          va        ='center'        ,
                          size      =10              ,
                          xytext    =(0, 8)          , 
                          textcoords='offset points')
            ymin, ymax = ax.get_ylim()
            
            ax.set_ylim(ymin,1.05*ymax)
    
    def barcounts(self,data,path="~/"):
        TITLE   = 0
        VALUES  = 1
        
        df     = data.select_dtypes(include='category')
        counts = []
        for c in df.columns:
            counts.append( (c,df[c].value_counts().to_dict()) )
        
        LEN     = len(counts)
        fcols   = self.math.sqrt(LEN)
        fcols   = self.math.ceil(fcols)
        frows   = self.math.ceil(LEN/fcols)
        
        fig = plt.figure(figsize=(14,9)); fig.subplots_adjust(hspace=0.4, wspace=0.4)
        for i,c in enumerate(counts):
            labels = list(c[VALUES].keys  ())
            values = list(c[VALUES].values())
            
            ax = fig.add_subplot(frows,fcols,i+1)
            g  = sns.barplot(x=labels, y=values, ax=ax)
            ax.set_title(c[TITLE])
            ax.grid(True)
            
            self._bar_annotate(ax,g,values)
        
        plt.savefig(path)
        plt.show()
            

class RelevancePlots():
    """docstring."""
    import seaborn as sns
    from matplotlib import pyplot as plt
    
    def __init__(self,target_name,prefix,PATH):
        self.plt.style.use('ggplot')
        plt.rcParams.update({'ytick.labelsize':10,'figure.figsize':(12,5)})
        self.EXT   = '.png'
        self.THRE  = 0.05
        
        self.target_name = target_name
        self.fname       = PATH+prefix+target_name+self.EXT
        
    def rf_relevanceplot(self,rf,features,save=True):
        imp  = rf.feature_importances_
        sort = imp.argsort()[::-1]
        #pdb.set_trace()
        g = self.sns.barplot(y=features[sort], x=imp[sort],color='seagreen')
        g.set_title(self.target_name)
        if save:
            self.plt.savefig(self.fname)
        else:
            self.plt.show()
        
        return {f:i for f,i in zip(features[sort],imp[sort])}
        
    def from_counts(self, counts, features, save=True):
        #TODO: use barplot of seaborn
        sort = counts.argsort()[::-1]
        
        g = self.sns.barplot(y=features[sort], x=counts[sort],color='seagreen')
        g.set_title(self.target_name)
        if save:
            self.plt.savefig(self.fname)
        else:
            self.plt.show()
        
        
