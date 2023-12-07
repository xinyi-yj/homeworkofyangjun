// 正式开始
// sysdir set PLUS "D:\Stata\Stata17\ado\plus"
// ssc install estout, replace
clear
import delimited "D:\myPyVenv\21377222\final\MICandNumber_alpha=0.68andn=80.csv"

egen mis = rowmiss(_all)

drop if mis

gen mic_sign = sign( pearson相关系数)* mic最大互信息系数

gen pearson_abs = abs( pearson相关系数 )

gen mic_pearson = mic最大互信息系数* pearson相关系数

gen mic_exp = exp( mic最大互信息系数)

gen pearson_exp = exp( pearson相关系数 )

// 验证 exp 的多重共线性
reg 弹幕占比 mic最大互信息系数 pearson相关系数 mic_sign pearson_abs mic_pearson mic_exp pearson_exp, robust level(95)

estat vif

// 验证 * 的多重共线性 
reg 弹幕占比 mic最大互信息系数 pearson相关系数 mic_sign pearson_abs mic_pearson, robust level(95)

estat vif

// 剔除之后回归
reg 弹幕占比 mic最大互信息系数 pearson相关系数 mic_sign pearson_abs, robust level(95)

estat vif

estimate store r1

esttab r1, b se star(+ 0.1 * 0.05 ** 0.01 *** 0.001)
// pr 出 pe 进 个人不建议步进（stata好像并不支持，他貌似只能输入或者剔除）
sw reg 弹幕占比 mic最大互信息系数 pearson相关系数 mic_sign pearson_abs mic_pearson, robust level(95) pr(0.1) pe(0.05)

estat vif

estimate store r2
// esttab r1,star(+ 0.1 * 0.05 ** 0.01 *** 0.001)
// 默认是 b 和 t ，b 换不掉

esttab r2, b se star(+ 0.1 * 0.05 ** 0.01 *** 0.001)