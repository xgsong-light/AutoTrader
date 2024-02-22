import backtrader as bt
import pandas as pd

from DataRepository.data_repository import DataRepository
from AnalyzerConfig.analyzers_config import analyzers_config

class BacktestEngine:
    def __init__(self, strategy, ts_code, period_type, initial_cash, analyzers_config):
        self.strategy = strategy
        self.ts_code = ts_code
        self.period_type = period_type
        self.initial_cash = initial_cash
        self.analyzers_config = analyzers_config
        self.cerebro = bt.Cerebro()

    def run(self):
        # 数据加载
        data_repo = DataRepository()
        data = data_repo.load_data(self.ts_code, self.period_type)
        if data is None:
            print(f"Failed to load data for {self.ts_code}")
            return None
        data = bt.feeds.PandasData(dataname=data)
        self.cerebro.adddata(data)

        # 添加策略
        self.cerebro.addstrategy(self.strategy)

        # 设置初始资金等
        self.cerebro.broker.setcash(self.initial_cash)

        # 添加分析器
        self.add_analyzers(self.cerebro, self.analyzers_config)

        # 运行回测
        self.results = self.cerebro.run()
        return self.results
    
    def add_analyzers(self, cerebro, config):
        for name, analyzer in config.items():
            if analyzer['enabled']:
                cerebro.addanalyzer(analyzer['analyzer'], _name=name, **analyzer['params'])