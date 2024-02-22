class ResultPresenter:
    def __init__(self, strategy, analyzers_config):
        self.strategy = strategy
        self.analyzers_config = analyzers_config

    def present(self):
        print("Backtest Results Analysis")
        print("========================")
        total_return = self.calculate_total_return()
        print(f'\nTotal Return: {total_return:.2f}%')

        annual_return = self.calculate_annual_return()
        print(f'Annual Return: {annual_return:.2f}%')

        win_rate = self.calculate_win_rate()
        print(f'Win Rate: {win_rate:.2f}%')

        for name, config in self.analyzers_config.items():
            if config['enabled']:
                analyzer = getattr(self.strategy.analyzers, name)
                print(f'\n{name.capitalize()} Analysis:')
                analysis = analyzer.get_analysis()
                self.print_analysis(analysis)

    def calculate_total_return(self):
        # Assumes the 'returns' analyzer is enabled and set as 'returns'
        returns_analyzer = self.strategy.analyzers.getbyname('returns')
        return returns_analyzer.get_analysis()['rtot'] * 100

    def calculate_annual_return(self):
        # Assumes the 'returns' analyzer is enabled and set as 'returns'
        returns_analyzer = self.strategy.analyzers.getbyname('returns')
        return returns_analyzer.get_analysis()['rnorm100']

    def calculate_win_rate(self):
        # Assumes the 'trade_analyzer' is enabled and set as 'trade_analyzer'
        trades = self.strategy.analyzers.trade_analyzer.get_analysis()
        total_trades = trades.total.closed
        if total_trades > 0:
            win_trades = trades.won.total
            return (win_trades / total_trades) * 100
        else:
            return 0
    
    @staticmethod
    def print_analysis(analysis):
        if isinstance(analysis, dict):
            for key, value in analysis.items():
                print(f'{key}: {value}')
        elif isinstance(analysis, (float, int)):
            print(f'Result: {analysis}')
        else:
            print(analysis)