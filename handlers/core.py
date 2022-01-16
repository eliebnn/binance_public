from binance_public.utils.misc import MiscUtils
from binance_public.enums import *

import datetime as dt
import pandas as pd
import os


class RequestCore:

    """RequestCore contains key attributes and generic functions for Bar and Tick child classes."""

    def __init__(self, trading_type='spot', symbols='BTCUSDT', years=None, months=None, intervals='1d',
                 start_date=None, end_date=None, folder=None, checksum=None):

        self.data_type = ''

        self.type = trading_type
        self.symbols = MiscUtils.obj_to_list(symbols)

        self.years = years if years else YEARS
        self.months = months if months else MONTHS
        self.intervals = MiscUtils.obj_to_list(intervals, True) if intervals else INTERVALS

        self.st_dt = start_date if start_date else (dt.datetime.now() + dt.timedelta(days=-1)).strftime('%Y-%m-%d')
        self.ed_dt = end_date if end_date else (dt.datetime.now() + dt.timedelta(days=-1)).strftime('%Y-%m-%d')

        self.folder = folder if folder else os.getcwd()
        self.checksum = checksum

    # ---

    @property
    def date_range(self):
        return self.st_dt + " " + self.ed_dt if self.st_dt and self.ed_dt else None

    @property
    def start_date(self):
        return START_DATE if not self.st_dt else MiscUtils.convert_to_date_object(self.st_dt)

    @property
    def end_date(self):
        return END_DATE if not self.ed_dt else MiscUtils.convert_to_date_object(self.ed_dt)

    @property
    def dates(self):
        return [d.strftime("%Y-%m-%d") for d in pd.date_range(start=self.start_date, end=self.end_date,
                                                              freq='D').to_pydatetime().tolist()]

    @staticmethod
    def to_dates(dates=None):

        dates = dates if dates else [d.strftime("%Y-%m-%d") for d in
                                     pd.date_range(end=dt.datetime.today(), periods=MAX_DAYS).to_pydatetime().tolist()]
        return MiscUtils.obj_to_list(dates, True)

    # ---

    @property
    def symbols_qty(self):
        return len(self.symbols)

    # ---

    def path(self, data_type='klines', period='daily', symbol=None, interval=None):
        return MiscUtils.get_path(self.type, data_type, period, symbol, interval)

    def daily_path(self, symbol=None, interval=None):
        return self.path(self.data_type, 'daily', symbol, interval)

    def monthly_path(self, symbol=None, interval=None):
        return self.path(self.data_type, 'monthly', symbol, interval)

    # ---

    def monthly_file(self, data_type, symbol, year, month, checksum=False):
        f = "{}-{}-{}-{}.zip".format(symbol.upper(), data_type, year, '{:02d}'.format(month))
        return f + '.CHECKSUM' if checksum else f

    def daily_file(self, data_type, symbol, date, checksum=False):
        f = "{}-{}-{}.zip".format(symbol.upper(), data_type, date)
        return f + '.CHECKSUM' if checksum else f
