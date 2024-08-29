import contextlib
import io
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.api import VAR

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'


class Aranger:
    def __init__(self, dataframe, lag_order=2, stability=True):
        """初始化"""
        # 输入dataframe
        self.df = dataframe
        # 默认滞后阶数为2
        self.lag_order = lag_order
        # 默认序列是平稳的
        self.stability = stability

    def set_origin_data(self):
        """原始数据初始设置"""
        # 将日期那一列转为datetime
        self.df['日期'] = pd.to_datetime(self.df['日期'])
        # 将日期设为index
        self.df.set_index('日期', inplace=True)
        # 设置日期频率，按日
        self.df.index = pd.date_range(start=self.df.index[0], periods=len(self.df), freq='D')

    def check_data_issues(self):
        """检查空值、无穷值、负数和零
            这里没写处理逻辑。
        """
        # 检查空值
        if self.df.isnull().values.any():
            print("存在空值。")
            print(self.df[self.df.isnull().any(axis=1)])

        # 检查无穷值
        if np.isinf(self.df.values).any():
            print("存在无穷值。")
            print(self.df[np.isinf(self.df).any(axis=1)])

        # 检查负数
        for col in self.df.columns:
            if (self.df[col] < 0).any():
                print(f"{col} 存在负数。")
                print(self.df[self.df[col] < 0])

        # 检查零
        for col in self.df.columns:
            if (self.df[col] == 0).any():
                print(f"{col} 存在零值。")
                print(self.df[self.df[col] == 0])

    def adf_check(self, data):
        """对选择的两个变量进行平稳性检验"""
        self.stability = True
        for col in data.columns:
            result = adfuller(data[col].dropna())  # 先移除缺失值，再ADF检验
            # print(result)
            print(f'{col}的ADF检验结果：')
            print(f'ADF统计量: {result[0]:.4f}')
            print(f'p值: {result[1]:.4f}')
            # 临界值格式化为4位小数
            critical_values = {k: f'{v:.4f}' for k, v in result[4].items()}
            print(f'临界值: {critical_values}')
            # 打印检验结论
            if result[1] < 0.01:
                print(f'结论: {col}在1%显著性水平下平稳')
            elif result[1] < 0.05:
                print(f'结论: {col}在5%显著性水平下平稳')
            elif result[1] < 0.1:
                print(f'结论: {col}在10%显著性水平下平稳')
            else:
                print(f'{YELLOW}结论: {col}不平稳:{RESET}')
                self.stability = False  # 只要有一列不平稳，就标记为不平稳
            print('-' * 50)

        # 如果任何列不平稳，则对所有列进行差分
        if not self.stability:
            print(f'{BLUE}差分后的ADF平稳性检验结果：:{RESET}')
            data = data.diff().dropna()  # 对所有列进行差分
            self.adf_check(data)  # 再次进行平稳性检验
            if not self.stability:
                print(f'{RED}差分后序列仍然不平稳，不建议进行Aranger相关性分析:{RESET}')
        return data

    def set_lag_order(self, data):
        """使用信息准则选择滞后阶数"""
        # 使用 VAR 模型选择滞后阶数
        model = VAR(data)
        lag_order = model.select_order()
        # print(lag_order)
        # 使用选择的滞后阶数进行 Granger 因果关系检验
        self.lag_order = min(lag_order.aic, lag_order.bic, lag_order.hqic, lag_order.fpe)
        print(f'{GREEN}选择的最小滞后阶数: {self.lag_order}:{RESET}')

    def granger_analysis(self, d1, d2):
        """Aranger检验"""
        # 选择要分析的2列
        data_to_analysis = self.df[[d1, d2]]
        # 检查数据有无异常值
        self.check_data_issues()
        # 对要分析的数据进行平稳性检验
        data_to_analysis = self.adf_check(data_to_analysis)
        # print(data_to_analysis.head(10))
        # TODO: 应该使用差分后的数据分析
        # 选择合适的滞后阶数
        self.set_lag_order(data_to_analysis)
        # 进行Aranger分析
        significant_lags = []  # 存储满足条件的滞后阶数
        # 屏蔽输出
        with contextlib.redirect_stdout(io.StringIO()):
            result = sm.tsa.stattools.grangercausalitytests(data_to_analysis, maxlag=self.lag_order)
        # 检查每个滞后阶数的 p 值
        for lag in range(1, self.lag_order + 1):
            test_result = result[lag][0]['ssr_ftest']  # 获取 F 检验结果
            p_value = test_result[1]  # p 值
            if p_value < 0.05:
                significant_lags.append(lag)
        return len(significant_lags) > 0

    def analysis_all(self):
        """对所有列，两两之间分析"""
        self.set_origin_data()
        col_names = self.df.columns.tolist()
        # 初始化相关性矩阵
        matrix = pd.DataFrame(0, index=col_names, columns=col_names)
        # 使用嵌套循环遍历所有可能的变量组合
        for i in range(len(col_names)):
            for j in range(i + 1, len(col_names)):
                var1 = col_names[i]
                var2 = col_names[j]
                print(f"分析 {var1} 与 {var2} 之间的 Granger 因果关系：")
                # 方向 var1 -> var2
                has_causality_1 = self.granger_analysis(var1, var2)
                # 方向 var2 -> var1
                has_causality_2 = self.granger_analysis(var2, var1)
                if has_causality_1:
                    matrix.loc[var1, var2] = 1
                    # matrix.loc[var2, var1] = 1
                if has_causality_2:
                    matrix.loc[var2, var1] = 1
                print('-' * 50)  # 分隔不同变量组合的输出
        print("Granger 因果关系矩阵：(行是因，列是果，对称位置都为1，则互为因果)")
        print(matrix)


if __name__ == '__main__':
    # 读取数据, 第二行开始
    df = pd.read_csv('上证指数.txt', encoding='ansi', sep=r'\s+', engine='python')
    analysis_obj = Aranger(df)
    analysis_obj.analysis_all()
