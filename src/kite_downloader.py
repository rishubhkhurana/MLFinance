import pandas as pd
import numpy as np
import datetime 
import logging
from kiteconnect import KiteConnect
from collections import defaultdict
import re
from selenium import webdriver
from fastprogress import progress_bar


API_KEY = "mbr5webseydvztcr"
API_SECRET = "53y7l441279l6m66j12sd8fpxn0ltmce"

def get_request_token():
    kite = KiteConnect(api_key="mbr5webseydvztcr")
    url=kite.login_url()

class KiteDownloader:
    def __init__(self,kite,exchange='NSE',instrument_type='EQ',savepath=''):
        self.kite,self.exchange = kite,exchange
        self.instrument_type = instrument_type
        self.savepath = savepath

    # get the list of all keys in every lement of returned list
    # insdict contains a list of defaultdict
    def convert_to_df(self,inpdict):
        cols_list=inpdict[0].keys()
        # initialize a dict with temporary elemnt as list
        tempdict = defaultdict(list)
        for row in inpdict:
            for k,v in row.items():
                tempdict[k].append(v)
        # crates a instruments dataframe
        return pd.DataFrame(tempdict)

    def get_available_instruments(self):
        insdict=self.kite.instruments()
        self.avail_inst = self.convert_to_df(insdict)
        

    def get_instrument_tokens(self,instlist=[]): 
        if len(instlist)>0:
            temp = self.avail_inst[np.logical_and(self.avail_inst.tradingsymbol.isin(instlist),self.avail_inst.exchange==self.exchange)]
        else:
            temp = self.avail_inst[np.logical_and(self.avail_inst.instrument_type==self.instrument_type,self.avail_inst.exchange==self.exchange)]
        token_list = temp['instrument_token'].tolist()
        token_symbols = temp['tradingsymbol'].tolist()
        return token_list,token_symbols

    # we need instrument token to get any kind of historical data from kite
    # following function with get the intrument token for pulling the records
    def get_instrument_token(self,pat,keyname=None,search_key='segment'):
        if not keyname is None:
            cond = self.avail_inst[search_key]==keyname
            cond = np.logical_and(cond,self.avail_inst["name"].apply(lambda x: True if pat.search(x) else False))
            temp = self.avail_inst.loc[cond]
        else:
            temp = self.avail_inst.loc[self.avail_inst["name"].apply(lambda x: True if pat.search(x) else False)]
        return temp['instrument_token'].values


    def download_data(self,instrument_token,from_date,to_date,interval='minute'):
        diff = (to_date-from_date).days
        temp=pd.DataFrame()
        if diff>60:
            for d in range(0,diff,60):
                from_date = sd + datetime.timedelta(d)
                hist=self.kite.historical_data(instrument_token,from_date=from_date,to_date=from_date+datetime.timedelta(60),interval=interval)
                if len(hist)==0:
                    break
                hist_df = self.convert_to_df(hist)
                temp=temp.append(hist_df)
        else:
            hist=self.kite.historical_data(instrument_token,from_date=from_date,to_date=to_date,interval=interval)
        if len(hist)>0:
            temp = self.convert_to_df(hist)
        return temp

    def get_hist_data(self,inst_tokens=[],inst_symbols=[],start_date='01/01/19',end_date='01/03/19',interval="minute"):
        sd = datetime.datetime.strptime(start_date,"%d/%m/%y")
        ed = datetime.datetime.strptime(end_date,"%d/%m/%y")
        self.all_data = []
        for symbol,token in progress_bar(zip(inst_symbols,inst_tokens)):
            temp = self.download_data(token,from_date=sd,to_date=ed,interval=interval)
            self.all_data.append((symbol,temp))
  
    def pre_filter(self,criteria='',**kwargs):
        """
        function to run suitable criteria to figure out the list of tradingsymbols to download data
        args--
        criteria: str or a callable function
        return list of trading symbols to download data on 
        """
        pass

    def run_downloader(self,start_date='01/01/2019',end_date='01/03/2019',interval='minute',pre_filter=False,criteria='',**kwargs):
        # get list of available tokens in kite
        self.get_available_instruments()
        # apply any filtering on the symbols to download data 
        if pre_filter:
            tradingsymb_list = self.filter_instruments(criteria=criteria,**kwargs)
        else:
            tradingsymb_list=[]
        #  get symbol and token numbers
        token_list,token_symbols = self.get_instrument_tokens(instlist=tradingsymb_list)
        # download data from kite
        self.get_hist_data()
    def save_data(self):
        pass
    
    def load_data(self):
        pass

  



