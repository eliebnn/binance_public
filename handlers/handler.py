from binance_public.handlers.tick_data import AggTrades, Trades
from binance_public.handlers.bar_data import KLines


class DataTypes:

    TYPES_MAP = {'aggTrades': AggTrades, 'klines': KLines, 'trades': Trades}

    @staticmethod
    def get_type(val):
        return DataTypes.TYPES_MAP.get(val, None)


class Binance:

    def __init__(self, trading_type='spot', data_type='trades', **kwargs):
        self.trading_type = trading_type
        self.data_type = data_type

        self.handler = DataTypes.get_type(val=data_type)(trading_type=trading_type, **kwargs)

    def get_daily_data(self, unzip=False, keep_unzip=False):
        return self.handler.get_daily_data(unzip=unzip, keep_unzip=keep_unzip)

    def get_monthly_data(self, unzip=False, keep_unzip=False):
        return self.handler.get_monthly_data(unzip=unzip, keep_unzip=keep_unzip)
