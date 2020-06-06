import pandas as pd
import numpy as np 
from pathlib import Path
import os

def get_ffme_returns(datapath = ''):
    """
    Load the Fama-French Dataset for the returns of the Top and Bottom Deciles by MarketCap
    """
    if not isinstance(datapath,(Path,str)):
        raise ValueError("datapath should either be of String type or Pathlib")
    if datapath=='':
        datapath = '../data'
    filepath = Path(datapath+'/Portfolios_Formed_on_ME_monthly_EW.csv')
    if not filepath.is_file():
        raise ValueError(f"File doesn't exist in the {datapath}")
    me_m = pd.read_csv(filepath,
                       header=0, index_col=0, na_values=-99.99)
    rets = me_m[['Lo 10', 'Hi 10']]
    rets.columns = ['SmallCap', 'LargeCap']
    rets = rets/100
    rets.index = pd.to_datetime(rets.index, format="%Y%m").to_period('M')
    return rets

def get_hfi_returns(datapath = ''):
    """
    Load and format the EDHEC Hedge Fund Index Returns
    """
    if not isinstance(datapath,(Path,str)):
        raise ValueError("datapath should either be of String type or Pathlib")
    if datapath=='':
        datapath = '../data'
    filepath = Path(datapath+'/edhec-hedgefundindices.csv')
    if not filepath.is_file():
        raise ValueError(f"File doesn't exist in the {datapath}")
    hfi = pd.read_csv(filepath,
                      header=0, index_col=0, parse_dates=True)
    hfi = hfi/100
    hfi.index = hfi.index.to_period('M')
    return hfi

def get_ind_file(filetype,datapath=''):
    """
    Load and format the Ken French 30 Industry Portfolios files
    """
    known_types = ["returns", "nfirms", "size"]
    if filetype not in known_types:
        raise ValueError(f"filetype must be one of:{','.join(known_types)}")
    if filetype is "returns":
        name = "vw_rets"
        divisor = 100
    elif filetype is "nfirms":
        name = "nfirms"
        divisor = 1
    elif filetype is "size":
        name = "size"
        divisor = 1
    filepath = Path(datapath+f'/ind30_m_{name}.csv')
    if not filepath.is_file():
        raise ValueError(f"File doesn't exist in the {datapath}")                 
    ind = pd.read_csv(filepath, header=0, index_col=0)/divisor
    ind.index = pd.to_datetime(ind.index, format="%Y%m").to_period('M')
    ind.columns = ind.columns.str.strip()
    return ind
                         
def get_ind_returns(datapath=''):
    """
    Load and format the Ken French 30 Industry Portfolios Value Weighted Monthly Returns
    """
    if not isinstance(datapath,(Path,str)):
        raise ValueError("datapath should either be of String type or Pathlib")
    if datapath=='':
        datapath = '../data'

    return get_ind_file("returns",datapath=datapath)

def get_ind_nfirms(datapath=''):
    """
    Load and format the Ken French 30 Industry Portfolios Average number of Firms
    """
    if not isinstance(datapath,(Path,str)):
        raise ValueError("datapath should either be of String type or Pathlib")
    if datapath=='':
        datapath = '../data'                     
    return get_ind_file("nfirms",datapath=datapath)

def get_ind_size(datapath=''):
    """
    Load and format the Ken French 30 Industry Portfolios Average size (market cap)
    """
    if not isinstance(datapath,(Path,str)):
        raise ValueError("datapath should either be of String type or Pathlib")
    if datapath=='':
        datapath = '../data'                     
    return get_ind_file("size",datapath=datapath)                       

def get_total_market_index_returns(datapath=''):
    """
    Load the 30 industry portfolio data and derive the returns of a capweighted total market index
    """
    ind_nfirms = get_ind_nfirms(datapath)
    ind_size = get_ind_size(datapath)
    ind_return = get_ind_returns(datapath)
    ind_mktcap = ind_nfirms * ind_size
    total_mktcap = ind_mktcap.sum(axis=1)
    ind_capweight = ind_mktcap.divide(total_mktcap, axis="rows")
    total_market_return = (ind_capweight * ind_return).sum(axis="columns")
    return total_market_return    
                         
 