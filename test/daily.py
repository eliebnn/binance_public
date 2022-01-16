from binance_public.handlers.handler import Binance

symbols = ['BTCUSDT', 'ETHUSDT']
st_dt = '2022-01-13'
ed_dt = '2022-01-14'
folder = None

bnb = Binance(data_type='aggTrades', symbols=symbols, start_date=st_dt, end_date=ed_dt, folder=folder)
bnb.get_daily_data(unzip=False, keep_unzip=False)

bnb = Binance(data_type='klines', symbols=symbols, start_date=st_dt, end_date=ed_dt, folder=folder)
bnb.get_daily_data(unzip=False, keep_unzip=False)

bnb = Binance(data_type='trades', symbols=symbols, start_date=st_dt, end_date=ed_dt, folder=folder)
bnb.get_daily_data(unzip=True, keep_unzip=False)

print()
