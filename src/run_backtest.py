# 引入必要的库
import backtrader as bt
from BacktestEngine.backtest_engine import BacktestEngine
from TradeStrategy.moving_average_strategy import MovingAverageStrategy
from ResultPresenter.result_presenter import ResultPresenter
from AnalyzerConfig.analyzers_config import analyzers_config

# 主程序
if __name__ == '__main__':
    # 配置初始条件
    ts_code = '000858.SZ'
    period_type = 'weekly'
    initial_cash = 10000.0

    # 实例化回测引擎，并设置初始资金
    backtest_engine = BacktestEngine(MovingAverageStrategy, ts_code, period_type, initial_cash, analyzers_config)

    # 运行回测
    backtest_results = backtest_engine.run()

    # 实例化结果输出模块，并展示结果
    presenter = ResultPresenter(backtest_results[0], analyzers_config)
    presenter.present()