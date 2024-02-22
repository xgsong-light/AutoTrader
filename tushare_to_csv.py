import tushare as ts
import pandas as pd
import os
import datetime

class TushareToCSV:
    def __init__(self, token):
        ts.set_token(token)
        self.pro = ts.pro_api()

    def fetch_data(self, ts_code, start_date, end_date):
        df = self.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        return df

    def process_data(self, df):
        columns_map = {
            'trade_date': 'Date',
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'vol': 'Volume'
        }
        df.rename(columns=columns_map, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
        df.sort_values(by='Date', inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    def resample_data(self, df, freq):
        df.set_index('Date', inplace=True)
        ohlc_dict = {
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum'
        }
        df_resampled = df.resample(freq).apply(ohlc_dict).dropna()
        df_resampled.reset_index(inplace=True)
        return df_resampled

    def save_to_csv(self, df, ts_code, period_type):
        # 确保data子目录存在
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # 文件名使用股票代码和周期类型
        filename = os.path.join(data_dir, f"{ts_code}_{period_type}.csv")
        
        # 保存为CSV文件
        df.to_csv(filename, index=False)
        print(f"Data has been successfully saved to {filename}")

    def run(self, ts_code, start_date, end_date):
        # 获取数据
        df_daily = self.fetch_data(ts_code, start_date, end_date)

        # 保存日线数据
        df_daily_processed = self.process_data(df_daily)
        self.save_to_csv(df_daily_processed, ts_code, 'daily')

        # 转换并保存周线数据
        df_weekly = self.resample_data(df_daily_processed.copy(), 'W-FRI')
        self.save_to_csv(df_weekly, ts_code, 'weekly')

        # 转换并保存月线数据
        df_monthly = self.resample_data(df_daily_processed.copy(), 'ME')
        self.save_to_csv(df_monthly, ts_code, 'monthly')

# 使用示例
if __name__ == '__main__':
    tushare_token = 'ebb9dae75ef5e4ce299b5ff4605d4ad6e63425b51271eed4828ed08c'
    tushare_to_csv = TushareToCSV(tushare_token)
    
    # 设置股票代码、开始结束日期
    start_date = '20100101'
    end_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y%m%d')
    
    # 000858.SZ = 五粮液，000651.SZ = 格力电器，000333.SZ = 美的集团，
    # 600519.SH = 贵州茅台，600036.SH = 招商银行
    stock_codes = ['000858.SZ', '000651.SZ', '000333.SZ', '600036.SH', '600519.SH']

    for code in stock_codes:
        tushare_to_csv.run(code, start_date, end_date)