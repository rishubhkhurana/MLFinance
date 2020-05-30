import pandas as pd
import datetime 
import logging
from kiteconnect import KiteConnect
from collections import defaultdict
import re



# get the list of all keys in every lement of returned list
# insdict contains a list of defaultdict
def convert_to_df(inpdict):
    cols_list=inpdict[0].keys()
    # initialize a dict with temporary elemnt as list
    tempdict = defaultdict(list)
    for row in inpdict:
        for k,v in row.items():
            tempdict[k].append(v)
    # crates a instruments dataframe
    return pd.DataFrame(tempdict)


def get_available_instruments(kite):
    insdict=kite.instruments()
    return convert_to_df(insdict)


# we need instrument token to get any kind of historical data from kite
# following function with get the intrument token for pulling the records
def get_instrument_token(df,pat,keyname=None,search_key='segment'):
    if not keyname is None:
        cond = df[search_key]==keyname
        cond = np.logical_and(cond,df["name"].apply(lambda x: True if pat.search(x) else False))
        temp = df.loc[cond]
    else:
        temp = df.loc[df["name"].apply(lambda x: True if pat.search(x) else False)]
    return temp['instrument_token'].values

def get_hist_data(kite,instrument_token,start_date='01/01/19',end_date='01/01/20',interval="minute"):
    sd = datetime.datetime.strptime(start_date,"%d/%m/%y")
    ed = datetime.datetime.strptime(end_date,"%d/%m/%y")
    diff = (ed-sd).days
    if diff>60:
        temp=pd.DataFrame()
        for d in range(0,diff,60):
            from_date = sd + datetime.timedelta(d)
            hist=kite.historical_data(instrument_token,from_date=from_date,to_date=from_date+datetime.timedelta(60),interval=interval)
            hist_df = convert_to_df(hist)
            temp=temp.append(hist_df)
    return temp