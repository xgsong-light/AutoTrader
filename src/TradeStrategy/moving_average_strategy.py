import backtrader as bt
from TradeStrategy.strategy_base import StrategyBase

class MovingAverageStrategy(StrategyBase):
    params = (
        ('sma1_period', 5),
        ('sma2_period', 10),
        ('sma3_period', 20),
        ('sma4_period', 30),
    )

    def __init__(self):
        # 初始化移动平均线指标
        self.sma1 = bt.indicators.SimpleMovingAverage(period=self.params.sma1_period)
        self.sma2 = bt.indicators.SimpleMovingAverage(period=self.params.sma2_period)
        self.sma3 = bt.indicators.SimpleMovingAverage(period=self.params.sma3_period)
        self.sma4 = bt.indicators.SimpleMovingAverage(period=self.params.sma4_period)
        
        # 用于判断加仓的标志
        self.added_position1 = False
        self.added_position2 = False

    def next(self):
        # 建仓信号：5日均线向上突破10日均线
        if self.sma1[0] > self.sma2[0] and self.sma1[-1] <= self.sma2[-1]:
            self.order_target_percent(target=0.3)

        # 加仓信号：5日均线向上突破20日均线
        if self.sma1[0] > self.sma3[0] and self.sma1[-1] <= self.sma3[-1] and not self.added_position1:
            self.order_target_percent(target=0.6)  # 累计仓位比例：30% + 30%
            self.added_position1 = True

        # 加仓信号：5日均线向上突破30日均线
        if self.sma1[0] > self.sma4[0] and self.sma1[-1] <= self.sma4[-1] and not self.added_position2:
            self.order_target_percent(target=0.8)  # 累计仓位比例：30% + 30% + 20%
            self.added_position2 = True

        # 止损信号：5日均线向下跌破10日均线
        if self.sma1[0] < self.sma2[0] and self.sma1[-1] >= self.sma2[-1]:
            self.order_target_percent(target=0.5 * self.broker.getposition(self.data).size / self.data.close[0])
            self.added_position1 = False  # 重置加仓标志

        # 止损信号：5日均线向下跌破20日均线
        if self.sma1[0] < self.sma3[0] and self.sma1[-1] >= self.sma3[-1]:
            self.order_target_percent(target=0)  # 清空所有仓位
            self.added_position1 = False  # 重置加仓标志1
            self.added_position2 = False  # 重置加仓标志2