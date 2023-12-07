import pandas as pd
from minepy import MINE
import os
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False  # 用来正常显示负号


# 用于计算MIC值和弹幕的整合数量占比
class MICNumberCalculate():
    def __init__(self): # 由于我是部分处理的，所以直接将路径放在里面了
        self.mine = MINE(alpha=0.6, c=15)

        self.df1 = pd.read_csv('D:/yuyin/speech-emotion.csv', low_memory=False, encoding='utf-8') # 主播端
        self.df2 = pd.read_csv('D:/myPyVenv/21377222/final/danmuemotion.csv', low_memory=False, encoding='utf-8') # 观众端
        self.df3 = pd.read_csv('D:/myPyVenv/21377222/final/numberOfDanmu.csv', low_memory=False, encoding='utf-8') # 弹幕数量 与 df2 的长度天然一致

        self.df1 = self.df1.sort_values(by='time')

        self.X = self.df1['情感指数'] # 主播端
        self.Y = self.df2['情感指数'] # 观众端
        self.Z = self.df3['d']
        # print(self.X)
        # print(self.Y)
        self.length = min(len(self.X), len(self.Y))
        if(len(self.X) > self.length): self.X = self.X[:self.length]
        if(len(self.Y) > self.length): self.Y = self.Y[:self.length], self.Z = self.Z[:self.length]
        # print(self.X)
        # print(self.Y)

    def mic_number_to_csv(self, number): # number 为数量
        # 计算MIC和弹幕数量
        MIC = []
        
        r = []

        Danmu = []
        i = number # 在判断时可以防止越界访问 后续对最后一个数据好操作
        while(i<self.length):
            x = self.X[i-number:i]
            y = self.Y[i-number:i]
            self.mine.compute_score(x, y)
            MIC.append(self.mine.mic())

            r.append(np.corrcoef(x,y)[0,1])

            Danmu.append(sum(self.Z[i-number:i]))
            i+=number
        x = self.X[i-number:] # 最后一个
        y = self.Y[i-number:]
        self.mine.compute_score(x, y)
        MIC.append(self.mine.mic())

        r.append(np.corrcoef(x,y)[0,1])

        Danmu.append(sum(self.Z[i-number:]))
        df = pd.DataFrame()
        df['MIC最大互信息系数'] = MIC

        df['Pearson相关系数'] = r

        df['弹幕数量'] = Danmu
        total_number = sum(Danmu)
        df['弹幕占比'] = df.apply(lambda row: 1.0*self.length*row['弹幕数量']/(total_number*number), axis=1)
        # 平均状态下为 1 看 相对于平均状态其程度
        # 对最后一个数据进行特殊处理
        df.at[df.index[-1], '弹幕占比'] = 1.0*self.length*Danmu[-1]/(total_number*(self.length-i+number))

        if(os.path.exists('D:/myPyVenv/21377222/final/MICandNumber.csv')):
            df.to_csv('D:/myPyVenv/21377222/final/MICandNumber.csv', mode='a', header=False, index=False, encoding='utf-8') # header 去掉追加的头
        else:
            df.to_csv('D:/myPyVenv/21377222/final/MICandNumber.csv', index=False, encoding='utf-8')
        
        self.mic_number() # 每计算一次都看看图

    def mic_number(self):
        df = pd.read_csv('D:/myPyVenv/21377222/final/MICandNumber.csv', low_memory=False, encoding='utf-8')
        fig = plt.figure()
        ax1=fig.subplots()
        ax2=ax1.twinx()

        ax1.plot(df.index.values, df['MIC最大互信息系数'].values, linestyle='-', label='MIC最大互信息系数', color='b')
        
        ax1.plot(df.index.values, df['Pearson相关系数'].values, linestyle='-', label='Pearson相关系数', color='g')
        ax1.legend(loc='upper left')

        ax2.plot(df.index.values, df['弹幕占比'].values, linestyle='--', label='弹幕占比', color='r')

        ax2.legend(loc='upper right')
        plt.show()
        

if __name__ == '__main__':
    micandnumbercalculate = MICNumberCalculate()
    micandnumbercalculate.mic_number_to_csv(number=40)