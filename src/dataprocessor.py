from regimports import *

_bar_map = {'time':get_time_bars,'volume':get_volume_bars,'dollar':get_dollar_bars,'dollar_imbalance':get_ema_dollar_imbalance_bars,
'volume_imbalance':get_ema_volume_imbalance_bars,'tick_imbalance':get_ema_tick_imbalance_bars,'dollar_run':get_ema_dollar_run_bars,'volume_run':get_ema_volume_run_bars,'tick_run':get_ema_tick_run_bars}

class InstrumentDataGenerator:
    def __init__(self,dataset):
        if len(dataset.all_data)==0:
            raise RuntimeError("Please download/load data in your  dataset's all_data object")
        self.raw_data = deepcopy(dataset.all_data)
        self.filter_data=None

    def post_filter(self,criteria=''):
        pass

    def generate_bars(self,typ='volume',**kwargs):
        if self.filter_data is None:
            func = _bar_map[typ]
            self.bar_data=[]
            for symbol,data in self.raw_data:
                temp=func(data,**kwargs)
                if isinstance(temp,[list,tuple]):
                    self.bar_data.append((symbol,temp))
    
    def run(self,criteria='',**kwargs):
        self.post_filter(criteria=criteria,**kwargs)
        self.generate_bars(**kwargs)


    


