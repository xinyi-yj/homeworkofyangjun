clear
import delimited "D:\myPyVenv\21377222\final\MICandNumber_alpha=0.68andn=80.csv"
// 剔除含nan值的行
egen mis = rowmiss(_all)

drop if mis
// 生成各mic和pearson的变形
gen mic_sign = sign( pearson相关系数)* mic最大互信息系数

gen pearson_abs = abs( pearson相关系数 )

// 没必要引入交叉项了 我认为
// gen mic_pearson = mic最大互信息系数* pearson相关系数

gen mic_exp = exp( mic最大互信息系数)

gen pearson_exp = exp( pearson相关系数 )

// 将所有变量加入模型做回归
reg 弹幕占比 mic最大互信息系数 pearson相关系数 mic_sign pearson_abs mic_exp pearson_exp, robust level(95)

estat vif