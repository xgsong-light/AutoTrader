import os
import csv
import matplotlib.pyplot as plt
from BacktestEngine.backtest_config import BacktestConfig

class ResultPresenter:
    def __init__(self, config, result):
        self.config = config
        self.result = result

    def present(self):
        self.present_analysis_result_to_csv()
        # self.present_analysis_result_in_chart()

    def present_backtest_info(self):
        print("\nBacktest Information:")
        print(f'TS Code: {self.config.ts_code}')
        print(f'Initial Cash: {self.config.initial_cash}')
        print(f'Strategy: {self.config.strategy.__name__}')

        return {
            'TS Code': self.config.ts_code,
            'Initial Cash': self.config.initial_cash,
            'Strategy': self.config.strategy.__name__
        }

    def present_returns(self):
        returns_analyzer = self.result.analyzers.getbyname('returns')
        total_cash = self.result.broker.get_value()
        total_return = returns_analyzer.get_analysis()['rtot'] * 100
        annual_return = returns_analyzer.get_analysis()['rnorm100']
        print("\nReturns Analysis:")
        print(f'Total Cash: {total_cash:.2f}')
        print(f'Total Return: {total_return:.2f}%')
        print(f'Annual Return: {annual_return:.2f}%')

        return {
            'Total Cash': total_cash,
            'Total Return': total_return,
            'Annual Return': annual_return
        }

    def present_drawdown(self):
        drawdown_analyzer = self.result.analyzers.getbyname('drawdown')
        max_drawdown = drawdown_analyzer.get_analysis()['max']['drawdown']
        moneydown = drawdown_analyzer.get_analysis()['max']['moneydown']
        length = drawdown_analyzer.get_analysis()['max']['len']
        print("\nDrawdown Analysis:")
        print(f'Max Drawdown: {max_drawdown:.2f}%')
        print(f'Max Moneydown: {moneydown:.2f}')
        print(f'Max Length: {length}')

        return {
            'Max Drawdown': max_drawdown,
            'Max Moneydown': moneydown,
            'Max Length': length
        }
    
    def present_sharpe_ratio(self):
        sharpe_ratio_analyzer = self.result.analyzers.getbyname('sharpe_ratio')
        print("\nSharpe Ratio Analysis:")
        print(f'Sharpe Ratio: {sharpe_ratio_analyzer.get_analysis()["sharperatio"]:.2f}')

        return {
            'Sharpe Ratio': sharpe_ratio_analyzer.get_analysis()["sharperatio"]
        }

    def present_win_rate(self):
        win_rate = self.calculate_win_rate()
        print("\nWin Rate Analysis:")
        print(f'Win Rate: {win_rate:.2f}%')

        return {        
            'Win Rate': win_rate
        }

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
        transactions_data = []
        for datetime, trans_list in transactions.items():
            for trans in trans_list:
                transaction_dict = {
                    'Date': datetime,  # Format datetime as a string
                    'Amount': trans[0],
                    'Price': trans[1],
                    'Sid': trans[2],
                    'Symbol': trans[3],
                    'Value': trans[4],
                }
                transactions_data.append(transaction_dict)
        return transactions_data
    
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

    def present_analysis_result_to_csv(self):
        # 确保结果目录存在
        result_dir = './ResultPresenter/result'
        os.makedirs(result_dir, exist_ok=True)

        # 构建文件名
        strategy_name = self.config.strategy.__name__
        filename = f'{self.config.ts_code}_{strategy_name}_{self.config.period_type}.csv'
        filepath = os.path.join(result_dir, filename)

        # 打开文件准备写入
        with open(filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            # 写入标题头
            writer.writerow(['Backtest Results Analysis'])

            # 写入分析结果
            writer.writerow(['TS Code', self.config.ts_code])
            writer.writerow(['Initial Cash', self.config.initial_cash])
            writer.writerow(['Strategy', strategy_name])

            # 可以调用各个present方法获取结果并写入，例如:
            self.write_analysis_to_csv(writer, 'Returns', self.present_returns())
            self.write_analysis_to_csv(writer, 'Drawdown', self.present_drawdown())
            self.write_analysis_to_csv(writer, 'Sharpe Ratio', self.present_sharpe_ratio())
            self.write_analysis_to_csv(writer, 'Win Rate', self.present_win_rate())

            transactions_data = self.present_transactions()  # 获取交易数据
            self.write_transactions_to_csv(writer, 'Transactions', transactions_data)

    def write_analysis_to_csv(self, writer, analysis_name, analysis_data):
        writer.writerow([analysis_name])
        for key, value in analysis_data.items():
            writer.writerow([key, value])
        writer.writerow([])  # 空行分隔不同的分析

    def write_transactions_to_csv(self, writer, analysis_name, transactions_data):
        writer.writerow([analysis_name])
        writer.writerow(['Date', 'Amount', 'Price', 'Sid', 'Symbol', 'Value'])  # 列标题
        for transaction in transactions_data:
            writer.writerow([transaction['Date'], transaction['Amount'], transaction['Price'], transaction['Sid'], transaction['Symbol'], transaction['Value']])
        writer.writerow([])  # 空行分隔不同的分析

    def present_analysis_result_in_chart(self):
        # 绘图设置 (可以自定义这些设置)
        plt.figure(figsize=(12, 6))
        
        # 绘制资产价值曲线
        plt.plot(self.result.analyzers.getbyname('time_return').get_analysis())
        
        # 添加标题和标签
        plt.title('Strategy Performance')
        plt.xlabel('Time')
        plt.ylabel('Portfolio Value')
        plt.grid(True)
        
        # 保存图表
        result_dir = './ResultPresenter/result'
        os.makedirs(result_dir, exist_ok=True)

        # 构建文件名
        strategy_name = self.config.strategy.__name__
        filename = f'{self.config.ts_code}_{strategy_name}_{self.config.period_type}_time_return.png'
        filepath = os.path.join(result_dir, filename)
        plt.savefig(filename)
        plt.show()  # 如果你希望在脚本运行时显示图表，可以取消注释这一行
        pass