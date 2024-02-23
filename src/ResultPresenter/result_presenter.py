from BacktestEngine.backtest_config import BacktestConfig

class ResultPresenter:
    def __init__(self, config, result):
        self.config = config
        self.result = result

    def present(self):
        self.custom_analysis_result()

    def custom_analysis_result(self):
        print("Backtest Results Analysis")
        print("========================")
        
        self.present_backtest_info()
        self.present_returns()
        self.present_drawdown()
        self.present_sharpe_ratio()
        self.present_win_rate()
        self.present_transactions()

    def present_backtest_info(self):
        print("\nBacktest Information:")
        print(f'TS Code: {self.config.ts_code}')
        print(f'Initial Cash: {self.config.initial_cash}')
        print(f'Strategy: {self.config.strategy.__name__}')

    def present_returns(self):
        returns_analyzer = self.result.analyzers.getbyname('returns')
        total_cash = self.result.broker.get_value()
        total_return = returns_analyzer.get_analysis()['rtot'] * 100
        annual_return = returns_analyzer.get_analysis()['rnorm100']
        print("\nReturns Analysis:")
        print(f'Total Cash: {total_cash:.2f}')
        print(f'Total Return: {total_return:.2f}%')
        print(f'Annual Return: {annual_return:.2f}%')

    def present_drawdown(self):
        drawdown_analyzer = self.result.analyzers.getbyname('drawdown')
        max_drawdown = drawdown_analyzer.get_analysis()['max']['drawdown']
        moneydown = drawdown_analyzer.get_analysis()['max']['moneydown']
        length = drawdown_analyzer.get_analysis()['max']['len']
        print("\nDrawdown Analysis:")
        print(f'Max Drawdown: {max_drawdown:.2f}%')
        print(f'Max Moneydown: {moneydown:.2f}')
        print(f'Max Length: {length}')
    
    def present_sharpe_ratio(self):
        sharpe_ratio_analyzer = self.result.analyzers.getbyname('sharpe_ratio')
        print("\nSharpe Ratio Analysis:")
        print(f'Sharpe Ratio: {sharpe_ratio_analyzer.get_analysis()["sharperatio"]:.2f}')

    def present_win_rate(self):
        win_rate = self.calculate_win_rate()
        print("\nWin Rate Analysis:")
        print(f'Win Rate: {win_rate:.2f}%')

    def calculate_win_rate(self):
        trades = self.result.analyzers.trade_analyzer.get_analysis()
        total_trades = trades.total.closed
        if total_trades > 0:
            win_trades = trades.won.total
            return (win_trades / total_trades) * 100
        else:
            return 0
        
    def present_transactions(self):
        transactions_analyzer = self.result.analyzers.getbyname('transactions')
        transactions = transactions_analyzer.get_analysis()
        print("\nTransactions Analysis:")
        self.print_analysis(transactions)
    
    def all_analysis_result(self):
        print("Backtest Results Analysis")
        for name, config in self.config.analyzers_config.items():
            if config['enabled']:
                analyzer = getattr(self.result.analyzers, name)
                print(f'\n{name.capitalize()} Analysis:')
                analysis = analyzer.get_analysis()
                self.print_analysis(analysis)

    @staticmethod
    def print_analysis(analysis):
        if isinstance(analysis, dict):
            for key, value in analysis.items():
                print(f'{key}: {value}')
        elif isinstance(analysis, (float, int)):
            print(f'Result: {analysis}')
        else:
            print(analysis)