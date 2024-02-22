import os
import pandas as pd
from DataRepository.file_manager import FileManager
from DataRepository.tushare_to_csv import TushareToCSV
import datetime

class DataRepository:
    def load_data(self, ts_code, period_type):
        filename = FileManager.filename(ts_code, period_type)
        if os.path.exists(filename):
            # 从文件中加载数据
            print(f"Loading data from {filename}")
            return self.load_data_from_csv(filename)
        else:
            # 从TuShare加载数据
            print(f"Loading data from TuShare for {ts_code}")
            self.load_data_from_tushare(ts_code)
            return None

    def load_data_from_csv(self, filename):
        # 从文件中加载数据
        if os.path.exists(filename):
            df = pd.read_csv(filename, index_col='Date', parse_dates=True)
            df = df.sort_index()  # 确保数据是按日期排序的
            # 如果需要，可以在这里对列名进行重命名，以确保它们与backtrader兼容
            # 例如：
            # df.rename(columns={'Open':'open', 'High':'high', ...}, inplace=True)
            return df
        else:
            return None
    
    def load_data_from_tushare(self, ts_code):
        # 从TuShare加载数据
        tushare_to_csv = TushareToCSV()
        start_date = '20100101'
        end_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
        tushare_to_csv.run(ts_code, start_date, end_date)