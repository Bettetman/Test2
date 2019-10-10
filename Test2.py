#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from  scipy.interpolate import lagrange

class Test2:
    __pathGetList = ["0","Resources/catering_sale_missing.xls",
                     "Resources/catering_sale_all.xls",
                     "Resources/normalization_data.xls",
                     "Resources/discretization_data.xls",
                  "Resources/sales_data.xls"]
    __pathOutList=["0","Output/missing_data_processing.xls","2","3",
                  "Output/data_descret.xls","5"]
    def Experiment1(self):
        x = pd.read_excel(self.__pathGetList[1])
        df = pd.DataFrame(x)
        lostList = []#存缺失的行
        lostnum = len(df)-df.count()["销量"]
        for i  in  range(len(df["销量"])):
            if np.isnan(df["销量"][i]):
                lostList.append(i)
        for lost in lostList:
           getNum = round(self.ployinterp_column(x["销量"], lost, k=3),1)
           print("缺失的行:",lost+1,"元素为:",getNum)
           x["销量"][lost] = getNum
        x.to_excel(self.__pathOutList[1])



    def Experiment2(self):
        x = pd.read_excel(self.__pathGetList[2])
        # print(x.shape,x.describe())
        # print("任意2个相关系数：")
        print(x.corr())#任意两款菜式之间的相关系数
        print(x.corr()[u"百合酱蒸凤爪"])#“百合酱蒸凤爪”与其他菜式的相关系数
        print(x[u'百合酱蒸凤爪'].corr(x[u'翡翠蒸香茜饺'])) # “百合酱蒸凤爪”与“翡翠蒸香茜饺”的相关系数



    def Experiment3(self):
        x = pd.read_excel(self.__pathGetList[3])
        data1 = (x - x.min()) / (x.max() - x.min())  # 最小-最大规范化
        data2 = (x - x.min()) / (x.std())  # 零-均值规范化
        data3 = x / 10 ** np.ceil(np.log10(x.abs().max()))  # 小数定标规范化
        print('最小-最大规范化', data1)
        print('零-均值规范化', data2)
        print('小数定标规范化', data3)


    def Experiment4(self):
        x = pd.read_excel(self.__pathGetList[4])
        u = x[u"肝气郁结症型系数"].copy()
        k = 4#离散系数
        d1 = pd.cut(u ,k,labels=range(k))
        print(d1)
        d1.to_excel(self.__pathOutList[4])


    # 用到的工具类
    def ployinterp_column(self,s, n, k):
        # 自定义列向量插值函数，s为列向量，n为被插值的位置,k为取前后的数据个数默认为5(此处取3)；
        y = s[list(range(n - k, n)) + list(range(n + 1, n + 1 + k))]
        y = y[y.notnull()]  # 剔除空值
        # lag = lagrange(y.index,list(y))-->lag,返回一个多项式系数列表
        # n为需要插入的index值
        return lagrange(y.index, list(y))(n)  # 插值并返回插值结果

if __name__ == '__main__':
    T  = Test2()
    T.Experiment4()
