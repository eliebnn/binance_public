from binance_public.handlers.handler import Binance

symbols = ['BTCUSDT', 'ETHUSDT']
symbols = ['BTCUSDT']
st_dt = '2022-01-13'
ed_dt = '2022-01-14'
folder = None

# SPOT EXAMPLeS

bnb = Binance(trading_type='futures', data_type='aggTrades', symbols=symbols, start_date=st_dt, end_date=ed_dt, folder=folder)
bnb.get_daily_data(unzip=False, keep_unzip=False)

bnb = Binance(data_type='klines', symbols=symbols, start_date=st_dt, end_date=ed_dt, folder=folder)
bnb.get_daily_data(unzip=False, keep_unzip=False)

bnb = Binance(trading_type='spot', data_type='trades', symbols=symbols, start_date=st_dt, end_date=ed_dt, folder=folder)
bnb.get_daily_data(unzip=True, keep_unzip=True)

# FUTURE EXAMPLE

bnb = Binance(trading_type='futures', data_type='trades', symbols=symbols, start_date=st_dt, end_date=ed_dt, folder=folder)
bnb.get_daily_data(unzip=True, keep_unzip=True)

print()
