import json

import scipy as sp
import pandas as pd
import numpy as np
import scipy.stats as stats

dict = {0: 9347, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 1080, 8: 582, 9: 450, 10: 889, 11: 571, 12: 679, 13: 712,
        14: 784, 15: 1149, 16: 918, 17: 1485, 18: 1365, 19: 1255, 20: 3674, 21: 2253, 22: 2424, 23: 2888, 24: 2953,
        25: 4171, 26: 3830, 27: 4478, 28: 4914, 29: 5007, 30: 7686, 31: 7268, 32: 8181, 33: 9313, 34: 10567, 35: 13553,
        36: 13980, 37: 16212, 38: 18499, 39: 21067, 40: 51384}
overallgpa = 32.37313217414929
overallcount = 235568
y = list(dict.values())
x = list(dict.keys())
df = pd.DataFrame()
df['gpa'] = x
df['count'] = y
df = df.T
avg = {}
frame = df
for entry in frame:
    # print(entry)
    count = df[entry]['count']
    grade = df[entry]['gpa']
    avg[grade] = count / overallcount
    # df['avg'] = count / overallcount
    # print(df[index])

    # avg = count / overallcount
    # index = y.index(count)
    # df[y]['gpa'] = avg
df = df.T
df['avg'] = avg
# df = df.T
# del df[0]
# del df[40]
# df = df.T
# print(avg)
# print(df)
# print(y)
# print(x)
sp.stats.describe(y)
import matplotlib.pyplot as plt
import seaborn as sns

fig, ax = plt.subplots(1, 1)
# print(stats.norm(df['avg']))
# print(stats.norm.stats(moments='mvsk'))
mean, var, skew, kurt = stats.norm.stats(moments='mvsk')
# sns.displot(df, x=df['avg'], kde=True, bins=41, color='darkblue', hist_kws={'edgecolor': 'black'},
#              kde_kws={'linewidth': 1}, )
# plt.hist(df, color='lightgreen', ec='black', bins=41)
# plt.show()
# sns.displot(
#   data=df,
#   x="gpa",
#   y="count",
#   col="Type",
#   kind="hist",
#   height=5,
#   aspect=1.2,
#   log_scale=(10,0),
#   bins=20
# # )
# df = df
# print(df)
# plot = sns.displot(x=df['gpa'],y=df['avg'], bins=41)
#
# plt.show()
# deterministic = deterministic_gen(name="deterministic")
# df['count'].cdf()



npoints = 4  # number of integer support points of the distribution minus 1
npointsh = npoints / 2
npointsf = float(npoints)
nbound = 4  # bounds for the truncated normal
normbound = (1 + 1 / npointsf) * nbound  # actual bounds of truncated normal
grid = df['count'].T
# integer grid
gridlimitsnorm = (grid - 0.5) / npointsh * nbound  # bin limits for the truncnorm
gridlimits = grid - 0.5  # used later in the analysis
grid = grid[:-1]
gridint = grid
print(grid)
probs = np.diff(stats.truncnorm.cdf(gridlimitsnorm, -normbound, normbound))
normdiscrete = stats.rv_discrete(values=(gridint,), name='normdiscrete')
print(
    'mean = %6.4f, variance = %6.4f, skew = %6.4f, kurtosis = %6.4f' % normdiscrete.stats(moments='mvsk'))
nd_std = np.sqrt(normdiscrete.stats(moments='v'))
print(nd_std)
n_sample = 41
rvs = normdiscrete.rvs(size=n_sample)
rvsnd = rvs
f, l = np.histogram(rvs, bins=gridlimits)
sfreq = np.vstack([gridint, f, probs*n_sample]).T
print(sfreq)
plt.show()