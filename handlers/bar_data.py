from binance_public.handlers.core import RequestCore
from binance_public.utils.getter import GetterUtils
from binance_public.utils.misc import MiscUtils
from enums import *


class Bar(RequestCore):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_type = 'bar'

    # ---

    def monthly_file(self, symbol, year, month, interval, checksum=False):
        f = "{}-{}-{}-{}.zip".format(symbol.upper(), interval, year, '{:02d}'.format(month))
        return f + '.CHECKSUM' if checksum else f

    def daily_file(self, symbol, date_val, interval, checksum=False):
        f = "{}-{}-{}.zip".format(symbol.upper(), interval, date_val)
        return f + '.CHECKSUM' if checksum else f

    # ---

    def get_monthly_data(self, unzip=False, keep_unzip=False):
        current = 0

        print("Found {} symbols".format(self.symbols_qty))

        for s in self.symbols:
            print("[{}/{}] - start download monthly {} klines ".format(current + 1, self.symbols_qty, s))

            for i in self.intervals:
                for y in self.years:
                    for m in self.months:

                        if self.start_date <= MiscUtils.convert_to_date_object(
                                '{}-{}-01'.format(y, m)) <= self.end_date:

                            file_name = self.monthly_file(s, y, m, i)
                            GetterUtils.download_file(self.monthly_path(s, i), file_name, self.folder,
                                                      unzip=unzip, keep_unzip=keep_unzip)

                            if self.checksum == 1:
                                checksum_file_name = self.monthly_file(s, y, m, i, checksum=True)
                                GetterUtils.download_file(self.monthly_path(s, i), checksum_file_name, self.folder)

            current += 1

    def get_daily_data(self, unzip=False, keep_unzip=False):
        current = 0

        print("Found {} symbols".format(self.symbols_qty))

        for s in self.symbols:
            print("[{}/{}] - start download daily {} klines ".format(current + 1, self.symbols_qty, s))

            for i in self.intervals:
                for d in self.dates:

                    if self.start_date <= MiscUtils.convert_to_date_object(d) <= self.end_date:

                        file_name = self.daily_file(s, d, i)
                        GetterUtils.download_file(self.daily_path(s, i), file_name, self.folder,
                                                  unzip=unzip, keep_unzip=keep_unzip)

                        if self.checksum == 1:
                            checksum_file_name = self.daily_file(s, d, i, checksum=True)
                            GetterUtils.download_file(self.daily_path(s, i), checksum_file_name, self.folder)

            current += 1


class KLines(Bar):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_type = 'klines'
