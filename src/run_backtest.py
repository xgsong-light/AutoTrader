# 引入必要的库
import backtrader as bt
from BacktestEngine.backtest_engine import BacktestEngine
from TradeStrategy.moving_average_strategy import MovingAverageStrategy
from ResultPresenter.result_presenter import ResultPresenter
from AnalyzerConfig.analyzers_config import analyzers_config
from BacktestEngine.backtest_config import BacktestConfig

# 主程序
if __name__ == '__main__':
    # 配置初始条件
    backtest_config = BacktestConfig('000858.SZ', 'monthly', 10000.0, MovingAverageStrategy, analyzers_config)

    # 实例化回测引擎
    backtest_engine = BacktestEngine(backtest_config)

    # 运行回测
    backtest_results = backtest_engine.run()

    # 实例化结果输出模块，并展示结果
    presenter = ResultPresenter(backtest_config, backtest_results[0])
    presenter.present()

    backtest_engine.plot()