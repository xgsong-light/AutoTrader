# analyzers_config.py
# 这是一个配置文件，可以作为模块被导入
import backtrader as bt

analyzers_config = {
    'sharpe_ratio': {
        'analyzer': bt.analyzers.SharpeRatio,
        'params': {'riskfreerate': 0.01},
        'enabled': True
    },
    'drawdown': {
        'analyzer': bt.analyzers.DrawDown,
        'params': {},
        'enabled': True
    },
    'returns': {
        'analyzer': bt.analyzers.Returns,
        'params': {},
        'enabled': True
    },
    'trade_analyzer': {
        'analyzer': bt.analyzers.TradeAnalyzer,
        'params': {},
        'enabled': True
    }
    # 其他分析器的配置可以在这里添加
}