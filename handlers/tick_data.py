from binance_public.handlers.core import RequestCore
from binance_public.utils.getter import GetterUtils
from binance_public.utils.misc import MiscUtils


class Tick(RequestCore):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_type = 'tick'

    # ---

    def monthly_file(self, symbol, year, month, checksum=False):
        return super().monthly_file(self.data_type,  symbol, year, month, checksum=checksum)

    def daily_file(self, symbol, date, checksum=False):
        return super().daily_file(self.data_type, symbol, date, checksum=checksum)

    # ---

    def get_monthly_data(self, unzip=False, keep_unzip=False):
        current = 0

        print("Found {} symbols".format(self.symbols_qty))

        for s in self.symbols:
            print("[{}/{}] - start download monthly {} {} ".format(current + 1, self.symbols_qty, s, self.data_type))

            for y in self.years:
                for m in self.months:

                    if self.start_date <= MiscUtils.convert_to_date_object('{}-{}-01'.format(y, m)) <= self.end_date:

                        file_name = self.monthly_file(s, y, m)
                        GetterUtils.download_file(self.monthly_path(s), file_name, self.folder,
                                                  unzip=unzip, keep_unzip=keep_unzip)

                        if self.checksum == 1:
                            checksum_file_name = self.monthly_file(s, y, m, checksum=True)
                            GetterUtils.download_file(self.monthly_path(s), checksum_file_name, self.folder)

            current += 1

    def get_daily_data(self, unzip=False, keep_unzip=False):
        current = 0

        print("Found {} symbols".format(self.symbols_qty))

        for s in self.symbols:
            print("[{}/{}] - start download daily {} {} ".format(current + 1, self.symbols_qty, s, self.data_type))

            for d in self.dates:

                if self.start_date <= MiscUtils.convert_to_date_object(d) <= self.end_date:
                    file_name = self.daily_file(s, d)
                    GetterUtils.download_file(self.daily_path(s), file_name, self.folder,
                                              unzip=unzip, keep_unzip=keep_unzip)

                    if self.checksum == 1:
                        checksum_file_name = self.daily_file(s, d, checksum=True)
                        GetterUtils.download_file(self.daily_path(s), checksum_file_name, self.folder)

            current += 1


class AggTrades(Tick):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_type = 'aggTrades'


class Trades(Tick):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_type = 'trades'
