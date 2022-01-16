import urllib.request
import zipfile
import json
import sys
import os

from pathlib import Path
from enums import *


class GetterUtils:

    @staticmethod
    def get_destination_dir(file_url, folder=None):
        store_directory = os.environ.get('STORE_DIRECTORY')
        if folder:
            store_directory = folder
        if not store_directory:
            store_directory = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(store_directory, file_url)

    @staticmethod
    def get_destination_dir_comp(_dir, _file, _folder=None):
        file_url = os.path.join(_dir, _file)
        return GetterUtils.get_destination_dir(file_url, _folder)

    @staticmethod
    def get_csv_dir(file_url):
        return os.path.join(file_url, 'csv')

    @staticmethod
    def get_download_url(file_url):
        return "{}{}".format(BASE_URL, file_url)

    @staticmethod
    def get_all_symbols(type):
        if type == 'um':
            response = urllib.request.urlopen("https://fapi.binance.com/fapi/v1/exchangeInfo").read()
        elif type == 'cm':
            response = urllib.request.urlopen("https://dapi.binance.com/dapi/v1/exchangeInfo").read()
        else:
            response = urllib.request.urlopen("https://api.binance.com/api/v3/exchangeInfo").read()
        return list(map(lambda symbol: symbol['symbol'], json.loads(response)['symbols']))

    @staticmethod
    def download_file(base_path, file_name, folder=None, unzip=False, keep_unzip=False):
        download_path = "{}{}".format(base_path, file_name)

        if folder:
            base_path = os.path.join(folder, base_path)

        save_path = GetterUtils.get_destination_dir(os.path.join(base_path, file_name), folder)

        if os.path.exists(save_path):
            print("\nfile already exists! {}".format(save_path))

        # make the directory
        if not os.path.exists(base_path):
            Path(GetterUtils.get_destination_dir(base_path)).mkdir(parents=True, exist_ok=True)

        try:
            if not os.path.exists(save_path):
                download_url = GetterUtils.get_download_url(download_path)
                dl_file = urllib.request.urlopen(download_url)
                length = dl_file.getheader('content-length')
                if length:
                    length = int(length)
                    blocksize = max(4096, length // 100)

                with open(save_path, 'wb') as out_file:
                    dl_progress = 0
                    print("\nFile Download: {}".format(save_path))
                    while True:
                        buf = dl_file.read(blocksize)
                        if not buf:
                            break
                        dl_progress += len(buf)
                        out_file.write(buf)
                        done = int(50 * dl_progress / length)
                        sys.stdout.write("\r[%s%s]" % ('#' * done, '.' * (50 - done)))
                        sys.stdout.flush()

        except urllib.error.HTTPError:
            print("\nFile not found: {}".format(download_url))
            pass

        if unzip:
            try:
                GetterUtils.unzip(base_path, file_name, folder)
            except Exception as e:
                print(e)

        if keep_unzip:
            try:
                os.remove(GetterUtils.get_destination_dir(os.path.join(base_path, file_name), folder))
            except Exception as e:
                print(e)

    @staticmethod
    def unzip(zip_path, zip_file_name, folder):

        csv_path = GetterUtils.get_csv_dir(zip_path)

        # make the directory
        if not os.path.exists(csv_path):
            Path(GetterUtils.get_destination_dir(csv_path)).mkdir(parents=True, exist_ok=True)

        zip_path = GetterUtils.get_destination_dir_comp(zip_path, zip_file_name, folder)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(csv_path)
