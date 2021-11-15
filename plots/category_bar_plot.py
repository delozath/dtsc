import pandas  as pd
import seaborn as sns

from matplotlib import pyplot as plt
from matplotlib import ticker

import pdb

def __config_bar_plots(ax, ncount):
    ax2    = ax.twinx()
    
    ax .yaxis.tick_right()
    ax .yaxis.set_label_position('right')
    ax2.yaxis.tick_left()
    ax2.yaxis.set_label_position('left')
    ax2.set_ylabel('Frequency [%]')
    
    for p in ax.patches:
        x=p.get_bbox().get_points()[:,0]
        y=p.get_bbox().get_points()[1,1]
        ax.annotate('{:.1f}%'.format(100.*y/ncount), (x.mean(), y), 
                ha='center', va='bottom')
        ax .set_ylim(0,ncount)
        ax2.set_ylim(0,100   )
        #ax2.yaxis.set_major_locator(ticker.MultipleLocator(10))
    
def category_bar_plot(data,figsize=(8,6),fname="",ext="png"):
    df     = data.select_dtypes(include='category')
    for cat in df.columns:
        fig,ax = plt.subplots(figsize=figsize)
        sns.countplot(x=cat, data=df, ax=ax)
        plt.title(f'{cat}')
        plt.xlabel('Counts')
        __config_bar_plots(ax, df.shape[0])
        if fname!="":
            plt.savefig(f"{fname}{cat}.{ext}")
    
    if fname=="":
        plt.show()

if __name__ == '__main__':
    main()