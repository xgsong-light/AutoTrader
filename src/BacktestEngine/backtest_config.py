from AnalyzerConfig.analyzers_config import analyzers_config

class BacktestConfig:
    def __init__(self, ts_code, period_type, initial_cash, strategy, analyzers_config):
        self.ts_code = ts_code
        self.period_type = period_type
        self.initial_cash = initial_cash
        self.strategy = strategy
        self.analyzers_config = analyzers_config