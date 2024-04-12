from datetime import datetime, timedelta
# import arch.unitroot as unitroot
import statsmodels.api as sm
import numpy as np
import pandas as pd
from scipy import stats
from typing import Union

def parse_freq(freq):
    """解析时间频率为timedelta对象"""
    unit = freq[-1]  # 获取时间单位
    if unit == 'm':
        return timedelta(minutes=int(freq[:-1]))
    elif unit == 'h':
        return timedelta(hours=int(freq[:-1]))
    elif unit == 'd':
        return timedelta(days=int(freq[:-1]))
    elif unit == 'w':
        return timedelta(weeks=int(freq[:-1]))
    elif unit == 'M':
        # 以30天计算一个月，因为timedelta没有月单位
        return timedelta(days=30*int(freq[:-1]))
    else:
        raise ValueError(f"Unsupported freq: {freq}")

def generate_time_periods(start_time, end_time, freq):
    """生成时间段列表"""
    delta = parse_freq(freq)
    current_time = start_time
    periods = []
    while current_time < end_time:
        next_time = min(current_time + delta, end_time)
        periods.append({
            "start_time": current_time,
            "end_time": next_time,
        })
        current_time = next_time
    return periods




def describeData(data: Union[pd.Series, pd.DataFrame], nan_policy:str = 'omit'):
    if isinstance(data, pd.DataFrame):
        sk = stats.skew(data, nan_policy=nan_policy)
        kurt = stats.kurtosis(data, nan_policy=nan_policy)
        sk_values = sk if isinstance(sk, np.ndarray) else sk.data
        kurt_values = kurt if isinstance(kurt, np.ndarray) else kurt.data
        describe_result = pd.concat([data.describe(),
            pd.DataFrame([sk_values], index=['skew'], columns=data.columns),
            pd.DataFrame([kurt_values], index=['kurtosis'], columns=data.columns)
        ])
        return describe_result
    elif isinstance(data, pd.Series):
        
        sk_values = stats.skew(data, nan_policy=nan_policy)
        kurt_values = stats.kurtosis(data, nan_policy=nan_policy)

        describe_result = data.describe()
        describe_result['skew'] = sk_values
        describe_result['kurtosis'] = kurt_values
        
        return describe_result      
    

# class TimeSeriesTool:
#     def getTableStatsDescribe(df, adf_max_lags=30, adf_method="BIC"):
#         _skew = df.apply(stats.skew)
#         _kurtosis = df.apply(stats.kurtosis)

#         return df.describe().append(
#             _skew.to_frame('skew').transpose()
#         ).append(
#             _kurtosis.to_frame('kurtosis').transpose()
#         ).append(TimeSeriesTool.unit_root_test(df, adf_max_lags=adf_max_lags, adf_method=adf_method))

#     def ADF_test(df, max_lags=10, method="BIC"):
#         """
#         trend : {'nc', 'c', 'ct', 'ctt'}, optional
#             The trend component to include in the ADF test
#             'nc' - No trend components
#             'c' - Include a constant (Default)
#             'ct' - Include a constant and linear time trend
#             'ctt' - Include a constant and linear and quadratic time trends
#         max_lags : int, optional
#             The maximum number of lags to use when selecting lag length
#         method : {'AIC', 'BIC', 't-stat'}, optional
#             The method to use when selecting the lag length
#             'AIC' - Select the minimum of the Akaike IC
#             'BIC' - Select the minimum of the Schwarz/Bayesian IC
#             't-stat' - Select the minimum of the Schwarz/Bayesian IC    
#         """
        
#         _all_adf = pd.DataFrame()
#         for col in df.columns:
#             #print("%s的 ADF單根檢定："%col)
#             _adf = unitroot.ADF(df.loc[:,col].values, max_lags = max_lags, method= method)
#             _temp_adf_df = pd.DataFrame([_adf.stat,
#                                         _adf.pvalue,
#                                         "%d"%_adf.lags], 
#                                         columns=[col],
#                 index=['ADF(max_lags=%s, method=%s) t-test'%(max_lags, method),
#                         'ADF(max_lags=%s, method=%s) p-value'%(max_lags, method),
#                         'ADF(max_lags=%s, method=%s) lags'%(max_lags, method),])
#             _all_adf = _all_adf.join(_temp_adf_df, how="outer")
#             #print(adf.summary().as_text())
#         return _all_adf

#     def PP_test(df):
#         _all_pp = pd.DataFrame()
#         for col in df.columns:
#             #print("%s的 ADF單根檢定："%col_name)
#             _pp = unitroot.PhillipsPerron(df.loc[:,col].values)
#             _temp_pp_df = pd.DataFrame([_pp.stat,
#                                         _pp.pvalue,
#                                         "%d"%_pp.lags], 
#                                         columns=[col],
#                 index=['PP t-test',
#                         'PP p-value',
#                         'PP lags'])
#             _all_pp = _all_pp.join(_temp_pp_df, how="outer")
#             #print(adf.summary().as_text())
#         return _all_pp
        
#     def KPSS_test(df):
#         _all_kpss = pd.DataFrame()
#         for col in df.columns:
#             #print("%s的 ADF單根檢定："%col_name)
#             _kpss = unitroot.KPSS(df.loc[:,col].values)
#             _temp_kpss_df = pd.DataFrame([_kpss.stat,
#                                         _kpss.pvalue,
#                                         "%d"%_kpss.lags], 
#                                         columns=[col],
#                 index=['kpss t-test',
#                         'kpss p-value',
#                         'kpss lags'])
#             _all_kpss = _all_kpss.join(_temp_kpss_df, how="outer")
#             #print(adf.summary().as_text())
#         return _all_kpss

#     def unit_root_test(df, adf_max_lags=30, adf_method="BIC"):
#         adf  = TimeSeriesTool.ADF_test(df, max_lags=adf_max_lags, method=adf_method)
#         pp   = TimeSeriesTool.PP_test(df)
#         kpss = TimeSeriesTool.KPSS_test(df)
#         all_unit_root_test = adf.append(pp).append(kpss)

#         _ur_list = []
#         for col_name in all_unit_root_test.columns:
#             temp = all_unit_root_test.loc[:, col_name]

#             _no_ur_count = 0
#             if temp[[idx_name for idx_name in all_unit_root_test.index if ("ADF" in idx_name) and ("p-value" in idx_name)][0]] <= 0.05:
#                 _no_ur_count += 1
#             if temp[[idx_name for idx_name in all_unit_root_test.index if ("PP" in idx_name) and ("p-value" in idx_name)][0]] <= 0.05:
#                 _no_ur_count += 1
#             if temp[[idx_name for idx_name in all_unit_root_test.index if ("kpss" in idx_name) and ("p-value" in idx_name)][0]] >= 0.05:
#                 _no_ur_count += 1

#             if _no_ur_count>=2:
#                 _ur_list.append("")
#             else:
#                 _ur_list.append("unit_root")
#         return all_unit_root_test.append(pd.DataFrame(_ur_list, index=all_unit_root_test.columns, columns=['is_unit_root']).transpose())

#     def getPACFLags(timeSeriesValues, method="ols", nlags=40, alpha=0.05):
#         pacf, pacf_confint=  sm.tsa.pacf(timeSeriesValues, method=method, nlags=nlags, alpha=alpha)
#         pacf_confint_interval = pacf_confint - pacf_confint.mean(1).reshape(-1, 1)
#         pacf_confint_interval_buttom, pacf_confint_interval_top = pacf_confint_interval.transpose()
#         return np.where((pacf >= pacf_confint_interval_top)|(pacf <= pacf_confint_interval_buttom))[0]
