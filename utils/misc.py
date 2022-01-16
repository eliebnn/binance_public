from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError
from typing import Iterable
from enums import *

import shutil
import os
import re


class MiscUtils:

    @staticmethod
    def convert_to_date_object(d):
        year, month, day = [int(x) for x in d.split('-')]
        date_obj = date(year, month, day)
        return date_obj

    @staticmethod
    def get_start_end_date_objects(date_range):
        start, end = date_range.split()
        start_date = MiscUtils.convert_to_date_object(start)
        end_date = MiscUtils.convert_to_date_object(end)
        return start_date, end_date

    @staticmethod
    def match_date_regex(arg_value, pat=re.compile(r'\d{4}-\d{2}-\d{2}')):
        if not pat.match(arg_value):
            raise ArgumentTypeError
        return arg_value

    @staticmethod
    def check_directory(arg_value):
        if os.path.exists(arg_value):
            while True:
                option = input('Folder already exists! Do you want to overwrite it? y/n  ')
                if option != 'y' and option != 'n':
                    print('Invalid Option!')
                    continue
                elif option == 'y':
                    shutil.rmtree(arg_value)
                    break
                else:
                    break
        return arg_value

    @staticmethod
    def get_path(trading_type, market_data_type, time_period, symbol, interval=None):
        trading_type_path = 'data/spot'
        if trading_type != 'spot':
            trading_type_path = f'data/futures/{trading_type}'
        if interval is not None:
            path = f'{trading_type_path}/{time_period}/{market_data_type}/{symbol.upper()}/{interval}/'
        else:
            path = f'{trading_type_path}/{time_period}/{market_data_type}/{symbol.upper()}/'
        return path

    @staticmethod
    def get_parser(parser_type):
        parser = ArgumentParser(description="This is a script to download historical {} data".format(parser_type),
                                formatter_class=RawTextHelpFormatter)
        parser.add_argument(
            '-s', dest='symbols', nargs='+',
            help='Single symbol or multiple symbols separated by space')
        parser.add_argument(
            '-y', dest='years', default=YEARS, nargs='+', choices=YEARS,
            help='Single year or multiple years separated by space\n-y 2019 2021 means to '
                 'download {} from 2019 and 2021'.format(
                parser_type))
        parser.add_argument(
            '-m', dest='months', default=MONTHS, nargs='+', type=int, choices=MONTHS,
            help='Single month or multiple months separated by space\n-m 2 12 means to download {} from '
                 'feb and dec'.format(
                parser_type))
        parser.add_argument(
            '-d', dest='dates', nargs='+', type=MiscUtils.match_date_regex,
            help='Date to download in [YYYY-MM-DD] format\nsingle date or multiple dates separated '
                 'by space\ndownload past 35 days if no argument is parsed')
        parser.add_argument(
            '-startDate', dest='startDate', type=MiscUtils.match_date_regex,
            help='Starting date to download in [YYYY-MM-DD] format')
        parser.add_argument(
            '-endDate', dest='endDate', type=MiscUtils.match_date_regex,
            help='Ending date to download in [YYYY-MM-DD] format')
        parser.add_argument(
            '-folder', dest='folder', type=MiscUtils.check_directory,
            help='Directory to store the downloaded data')
        parser.add_argument(
            '-c', dest='checksum', default=0, type=int, choices=[0, 1],
            help='1 to download checksum file, default 0')
        parser.add_argument(
            '-t', dest='type', default='spot', choices=TRADING_TYPE,
            help='Valid trading types: {}'.format(TRADING_TYPE))

        if parser_type == 'klines':
            parser.add_argument(
                '-i', dest='intervals', default=INTERVALS, nargs='+', choices=INTERVALS,
                help='single kline interval or multiple intervals separated by space\n-i 1m 1w '
                     'means to download klines interval of 1minute and 1week')

        return parser

    @staticmethod
    def obj_to_list(obj, drop_duplicates=False):
        if obj is None:
            return None
        elif isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float):
            return [obj]
        elif isinstance(obj, set):
            return [x for x in obj]
        elif isinstance(obj, list):
            return list(sorted(set(obj))) if drop_duplicates else obj
        # Catch-all for any other iterable
        elif isinstance(obj, Iterable):
            return list(sorted(set(obj))) if drop_duplicates else list(obj)
        else:
            raise TypeError("This type appears wrong and we don't know how to use it")
