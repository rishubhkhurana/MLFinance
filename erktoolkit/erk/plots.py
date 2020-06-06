import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_moving_average(df,typ,**kwargs):
    if not 'figsize' in kwargs:
        kwargs['figsize'] = (16,8)
    if not isinstance(df,(pd.Series,pd.DataFrame)):
        raise ValueError("df should be an instance of either Series of DataFrame")
    if typ not in ['simple','exp','both']:
        raise ValueError("typ should be either simple,exp or both")
    df.plot(figsize=kwargs['figsize'])
    if typ=='simple':
        df.rolling(window=kwargs['window'] if 'window' in kwargs else 36).mean().plot()
    elif typ=='exp':
        df.ewm(alpha = kwargs['alpha'] if 'alpha' in kwargs else 0.1).mean().plot()
    else:
        df.rolling(window=kwargs['window'] if 'window' in kwargs else 36).mean().plot()
        df.ewm(alpha = kwargs['alpha'] if 'alpha' in kwargs else 0.1).mean().plot()
