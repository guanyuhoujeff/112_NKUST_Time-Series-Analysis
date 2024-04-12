from binance.spot import Spot
from binance.cm_futures import CMFutures
import pandas as pd
from datetime import datetime, timedelta

def parser_k_line_data(klines_data) -> pd.DataFrame:
    #     1499040000000,      // k线开盘时间
    #     "0.01634790",       // 开盘价
    #     "0.80000000",       // 最高价
    #     "0.01575800",       // 最低价
    #     "0.01577100",       // 收盘价(当前K线未结束的即为最新价)
    #     "148976.11427815",  // 成交量
    #     1499644799999,      // k线收盘时间
    #     "2434.19055334",    // 成交额
    #     308,                // 成交笔数
    #     "1756.87402397",    // 主动买入成交量
    #     "28.46694368",      // 主动买入成交额
    #     "17928899.62484339" // 请忽略该参数
    klines_table = pd.DataFrame(klines_data, columns=[
        'open_time',
        'open',
        'high',
        'low',
        'close',
        'volume',
        'close_time',
        'amount',
        'count',
        'take_volume',
        'take_amount',
        '_'
    ])
    
    klines_table['open'] = klines_table['open'].astype(float)
    klines_table['high'] = klines_table['high'].astype(float)
    klines_table['low'] = klines_table['low'].astype(float)
    klines_table['close'] = klines_table['close'].astype(float)
    klines_table['volume'] = klines_table['volume'].astype(float)
    
    klines_table['amount'] = klines_table['amount'].astype(float)
    klines_table['count'] = klines_table['count'].astype(int)
    
    klines_table['take_volume'] = klines_table['take_volume'].astype(float)
    klines_table['take_amount'] = klines_table['take_amount'].astype(float)
    
    klines_table['open_time'] = klines_table['open_time'].apply(lambda x: datetime.fromtimestamp(int(x)/1000))
    klines_table['close_time'] = klines_table['close_time'].apply(lambda x: datetime.fromtimestamp(int(x)/1000))
    return klines_table.sort_values('open_time')

class DataManager:
    def __init__(self, api_key, api_secret) -> None:
        self._spot_client = Spot(
            api_key=api_key, 
            api_secret=api_secret
        )

        self._futures_client = CMFutures(
            key=api_key, 
            secret=api_secret
        )

    def getKlinesTable(self, **kwargs) -> pd.DataFrame:
        klines = self._spot_client.klines(**kwargs)
        return parser_k_line_data(klines)


    def getFKlinesTable(self, **kwargs) -> pd.DataFrame:
        klines = self._futures_client.klines(**kwargs)
        return parser_k_line_data(klines)
    
    @property
    def spot_client(self): return self._spot_client
    
    @property
    def futures_client(self): return self._futures_client