from binance_public.handlers.handler import Binance

trading_type = None
symbols = None
num_symbols = 1
# dates = ['2022-01-14']
dates = None
st_dt = '2022-01-13'
ed_dt = '2022-01-14'
folder = None
checksum = 1

bnb = Binance(data_type='aggTrades', symbols=['BTCUSDT', 'ETHUSDT'], start_date=st_dt, end_date=ed_dt)
bnb.get_monthly_data(unzip=False, keep_unzip=False)

bnb = Binance(data_type='klines', symbols=['BTCUSDT', 'ETHUSDT'], start_date=st_dt, end_date=ed_dt)
bnb.get_monthly_data(unzip=False, keep_unzip=False)

bnb = Binance(data_type='trades', symbols=['BTCUSDT', 'ETHUSDT'], start_date=st_dt, end_date=ed_dt)
bnb.get_monthly_data(unzip=False, keep_unzip=False)

print()
