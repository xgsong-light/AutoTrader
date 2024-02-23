import backtrader as bt
import pandas as pd

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
    
    def add_analyzers(self, cerebro, config):
        for name, analyzer in config.items():
            if analyzer['enabled']:
                cerebro.addanalyzer(analyzer['analyzer'], _name=name, **analyzer['params'])