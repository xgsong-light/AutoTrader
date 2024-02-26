import backtrader as bt
import pandas as pd
import os
import matplotlib

from DataRepository.data_repository import DataRepository
from AnalyzerConfig.analyzers_config import analyzers_config
from BacktestEngine.backtest_config import BacktestConfig

class BacktestEngine:
    def __init__(self, config):
        self.config = config
        self.cerebro = bt.Cerebro()

    def run(self):
        # 数据加载
        data_repo = DataRepository()
        data = data_repo.load_data(self.config.ts_code, self.config.period_type)
        if data is None:
            print(f"Failed to load data for {self.config.ts_code}")
            return None
        data = bt.feeds.PandasData(dataname=data)
        self.cerebro.adddata(data)

        # 添加策略
        self.cerebro.addstrategy(self.config.strategy)

        # 设置初始资金等
        self.cerebro.broker.setcash(self.config.initial_cash)

        # 添加分析器
        self.add_analyzers(self.cerebro, self.config.analyzers_config)

        # 运行回测
        self.results = self.cerebro.run()
        return self.results
    
    def plot(self):
        
        # 构建文件名
        strategy_name = self.config.strategy.__name__
        filename = f'{self.config.ts_code}_{strategy_name}_{self.config.period_type}'

        # 获取当前文件的上一级目录
        relative_path_to_result_dir = os.path.join(os.path.pardir, 'src/ResultPresenter/result')
        
        # 目标文件夹的名称
        absolute_path_to_result_dir = os.path.abspath(relative_path_to_result_dir)
        
        # 构建目标文件夹的完整路径
        if not os.path.exists(absolute_path_to_result_dir):
            os.makedirs(absolute_path_to_result_dir)
        
        # 构建保存图表的完整路径
        file_path = os.path.join(absolute_path_to_result_dir, filename)

        # 判断是否有图形界面环境，如果没有，使用无图形后端
        if not matplotlib.get_backend():
            matplotlib.use('Agg')
        
        # 绘制图表并保存到文件
        try:
            self.cerebro.plot(style='candlestick', savefig=dict(fname=file_path, dpi=100, tight_layout=True))
            print(f"图表已保存为文件：{file_path}")
        except Exception as e:
            print(f"An error occurred while saving the plot: {e}")

    
    def add_analyzers(self, cerebro, config):
        for name, analyzer in config.items():
            if analyzer['enabled']:
                cerebro.addanalyzer(analyzer['analyzer'], _name=name, **analyzer['params'])