import pandas as pd
import numpy as np
import cvxpy as cp
from scipy import stats


# 数据预处理
indexes = pd.read_excel("【笔试】基于净值的基金评价.xlsx", sheet_name="巨潮风格指数")
funds = pd.read_excel("【笔试】基于净值的基金评价.xlsx", sheet_name="基金净值")
indexes.drop(index=0, inplace=True)
funds.drop(index=0, inplace=True)
indexes.set_index("日期", inplace=True)
funds.set_index("日期", inplace=True)
funds.dropna(axis=0, how="all", inplace=True)

# Sharpe方法 最后结果分不同基金输出成了三个csv
def Sharpe(funds, indexes):
    # 风格指数种类选择 大盘成长,大盘价值,中盘成长,中盘价值,小盘成长,小盘价值,中证全债
    indexes_name = ["大盘成长", "大盘价值", "中盘成长", "中盘价值", "小盘成长", "小盘价值", "中债总财富指数"]
    indexes_selected = indexes[indexes_name]
    # 计算收益率
    funds_return_rate = (funds - funds.shift(1)) / funds.shift(1)
    funds_return_rate.dropna(axis=0, how="all", inplace=True)
    indexes_Sharp_return_rate = (indexes_selected - indexes_selected.shift(1)) / indexes_selected.shift(1)
    indexes_Sharp_return_rate.dropna(axis=0, how="all", inplace=True)

    funds_name = list(funds_return_rate.columns)
    Sharpe_result = pd.DataFrame(index=indexes_name).T

    # 用来进行Sharpe分析的函数，fund_Q是基金的一个季度的收益率
    def apply_Sharpe(fund_Q):
        indexes_Q = indexes_Sharp_return_rate.loc[fund_Q.index]

        # 利用cvxpy求解最优化问题
        # 基金收益率
        R = np.array(fund_Q)
        F = np.array(indexes_Q)
        # 待优化的回归系数
        b = cp.Variable(indexes_Q.shape[1])
        # 目标函数，最小化均方误差
        objective = cp.Minimize(cp.sum_squares(F @ b - R))
        # 约束条件，权重在[0,1]之间，权重之和为1
        constraints = [0 <= b, b <= 1, cp.sum(b) == 1]
        prob = cp.Problem(objective, constraints)
        result = prob.solve()

        # 用得出的线性模型计算得到的y值
        y_line = np.matmul(F, np.array(b.value).reshape(-1,1))
        # 实际上的y值
        y = R
        # 估计标准误差
        se = np.sqrt(np.sum(np.square(y-y_line)) / (y.size - 2))
        t_statistic = np.zeros(F.shape[1])
        p = np.zeros(F.shape[1])
        for i in range(F.shape[1]):
            x = F[:,i]
            # 计算t统计量,双边检测加绝对值
            t_statistic[i] = np.abs(se/(np.sum(np.power(x,2)) + ((np.sum(x) ** 2)/(y.size))))
            # 计算t统计量对应的p值，Sharpe无截距项，所以自由度少减去1
            p[i] = stats.t.sf(t_statistic[i], F.shape[0] - F.shape[1])
        # print(t_statistic)
        # 现在既有线性模型参数又有是否显著，对结果赋值
        end_date = fund_Q.index[-1]
        for i,name in enumerate(list(indexes_Q.columns)):
            # ***表示通过1%显著水平，**表示通过5%显著水平，*表示通过10%显著水平
            # Sharpe_result.loc[end_date, name] = str(round((b.value)[i],4)) + ('*' if p[i] < 0.1 else "") + \
            #                                     ('*' if p[i] < 0.05 else "") + ('*' if p[i] < 0.01 else "")
            # 双边检测
            Sharpe_result.loc[end_date, name] = str(round((b.value)[i], 4)) + ('*' if p[i] < 0.5 else "") + \
                                                ('*' if p[i] < 0.025 else "") + ('*' if p[i] < 0.005 else "")

        # Sharpe_result.loc[end_date] = list(map(lambda x: round(x, 4), b.value))

    # 按基金名称循环处理
    for fund_name in funds_name:
        fund_return_rate = funds_return_rate[fund_name]
        fund_return_rate.dropna(axis=0, how="all", inplace=True)
        # 以季度为频率进行Sharpe分析
        fund_return_rate.resample('Q').apply(apply_Sharpe)
        Sharpe_result.to_csv("Sharpe" + fund_name + ".csv", encoding="gbk")
        Sharpe_result = pd.DataFrame(index=indexes_name).T

Sharpe(funds, indexes)

def Fama(funds, indexes):
    # 年化无风险收益率
    risk_free = 0.015
    risk_free = ((1 + risk_free) ** (1/365)) - 1
    # 风格指数种类选择 万得全A（用来计算市场收益率） 巨潮大盘,巨潮小盘（用来计算SMB） 巨潮成长,巨潮价值（用来计算HML）
    indexes_name = ["万得全A","巨潮大盘","巨潮小盘","巨潮成长","巨潮价值"]
    indexes_selected = indexes[indexes_name]
    # 计算收益率
    funds_return_rate = (funds - funds.shift(1)) / funds.shift(1)
    funds_return_rate -= risk_free
    funds_return_rate.dropna(axis=0, how="all", inplace=True)
    indexes_Fama_return_rate = (indexes_selected - indexes_selected.shift(1)) / indexes_selected.shift(1)
    indexes_Fama_return_rate.dropna(axis=0, how="all", inplace=True)
    # 计算市场收益率部分
    indexes_Fama_return_rate["万得全A"] -= risk_free
    # 计算SMB
    indexes_Fama_return_rate["SMB"] = indexes_Fama_return_rate["巨潮小盘"] - indexes_Fama_return_rate["巨潮大盘"]
    # 计算HML
    indexes_Fama_return_rate["HML"] = indexes_Fama_return_rate["巨潮成长"] - indexes_Fama_return_rate["巨潮价值"]
    indexes_Fama_return_rate = indexes_Fama_return_rate[["万得全A", "SMB", "HML"]]
    # 截距项
    indexes_Fama_return_rate["alpha"] = 1

    funds_name = list(funds_return_rate.columns)
    Fama_result = pd.DataFrame(index=list(indexes_Fama_return_rate.columns)).T


    # 用来进行Fama三因子分析的函数，fund_Q是基金的一个季度的收益率
    def apply_Fama(fund_Q):
        indexes_Q = indexes_Fama_return_rate.loc[fund_Q.index]

        # 利用cvxpy求解最优化问题
        # 基金收益率
        R = np.array(fund_Q)
        F = np.array(indexes_Q)
        # 待优化的回归系数
        b = cp.Variable(indexes_Q.shape[1])
        # 目标函数，最小化均方误差
        objective = cp.Minimize(cp.sum_squares(F @ b - R))
        prob = cp.Problem(objective)
        result = prob.solve()

        # 用得出的线性模型计算得到的y值
        y_line = np.matmul(F, np.array(b.value).reshape(-1, 1))
        # 实际上的y值
        y = R
        # 估计标准误差
        se = np.sqrt(np.sum(np.square(y - y_line)) / (y.size - 2))
        t_statistic = np.zeros(F.shape[1])
        p = np.zeros(F.shape[1])
        for i in range(F.shape[1]):
            x = F[:, i]
            # 计算t统计量
            t_statistic[i] = np.abs(se / (np.sum(np.power(x, 2)) + ((np.sum(x) ** 2) / (y.size))))
            # 计算t统计量对应的p值，有截距，自由度多减去1
            p[i] = stats.t.sf(t_statistic[i], F.shape[0] - F.shape[1] - 1)
        # print(t_statistic)
        end_date = fund_Q.index[-1]
        for i,name in enumerate(list(indexes_Q.columns)):
            # ***表示通过1%显著水平，**表示通过5%显著水平，*表示通过10%显著水平
            # Fama_result.loc[end_date, name] = str(round((b.value)[i],4)) + ('*' if p[i] < 0.1 else "") + \
            #                                     ('*' if p[i] < 0.05 else "") + ('*' if p[i] < 0.01 else "")
            Fama_result.loc[end_date, name] = str(round((b.value)[i], 4)) + ('*' if p[i] < 0.05 else "") + \
                                              ('*' if p[i] < 0.025 else "") + ('*' if p[i] < 0.005 else "")
        # Fama_result.loc[end_date] = list(map(lambda x: round(x, 4), b.value))

    # 按基金名称循环处理
    for fund_name in funds_name:
        fund_return_rate = funds_return_rate[fund_name]
        fund_return_rate.dropna(axis=0, how="all", inplace=True)
        # 以季度为频率进行Sharpe分析
        fund_return_rate.resample('Q').apply(apply_Fama)
        Fama_result.to_csv("Fama" + fund_name + ".csv", encoding="gbk")
        Fama_result = pd.DataFrame(index=list(indexes_Fama_return_rate.columns)).T

Fama(funds, indexes)


