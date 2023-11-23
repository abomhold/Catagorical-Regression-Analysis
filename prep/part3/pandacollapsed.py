import random

import numpy as np
import numpy.random
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split

gpa_dict = eval(open('../old/percents', 'r').read())
df = pd.DataFrame(gpa_dict)
df.index = df.index.astype(int)
df = df.sort_index(ascending=True)
# print(df)

# df=df.T
# x = df.index
#y = df
# print(df)
# print(x)
# for d in df.T.values:

     #plt.boxplot(x, d, color='red')
plt.style.use('_mpl-gallery')
np.random.seed(1)
# make data:
x = df.index
y = df.values

# plot:
# fig, ax = plt.subplots()
# vp = ax.violinplot(x, y, widths=2,
#                    showmeans=False, showmedians=False, showextrema=False)
# #ax.eventplot(y, orientation="vertical", lineoffsets=x, linewidth=0.75)
#
# ax.set(xlim=(0, 40), xticks=np.arange(1, 39),
#        ylim=(0, 1), yticks=np.arange(0, 1))
#
# plt.show()

np.random.seed(1)
x = np.random.randn(5000)
y = 1.2 * x + np.random.randn(5000) / 3
print(x)
print(y)
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.003, random_state=random.randint(0,4294967295))
# pt = preprocessing.PowerTransformer(method='yeo-johnson', standardize=False)
# y_test = pt.fit_transform(y_test)
# y_train = pt.fit_transform(y_train)
# print(x_train)
# print(x_test)
# print(y_train)
# print(y_test)
# #
# from sklearn.decomposition import PCA
#
# # #
# pca = PCA(n_components=1)
# y_train = pca.fit_transform(y_train)
# print(y_train)
# y_test = pca.fit_transform(y_test)
# print(y_test)
# explained_variance = pca.explained_variance_ratio_
# print(explained_variance)
# # #
# from sklearn.linear_model import LogisticRegression

# # #
# model = LogisticRegression(random_state=0, max_iter=1000, solver='liblinear')  # You can try different solvers like 'liblinear', 'newton-cg', etc.
# model.fit(y_train)
# print(model)
# y = model.predict(x_test)
#plt.scatter(x_test, y_test, color='red')
# plt.figure(1, figsize=(4, 3))
# plt.clf()
# plt.plot(y_train, x_train, color="black", marker='+')
#plt.show()
#
# # y_pred = classifier.predict(y_test)
# # print(y_pred)
# # Evaluate the model...
# from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
#
# # # Assume y_test are your true labels and y_pred are the predictions from the logistic regression model
# # x_pred = classifier.predict(x_test)
#
# # # Confusion Matrix
# # conf_matrix = confusion_matrix(x_train, x_pred)
# # print(f"Confusion Matrix:\n{conf_matrix}")
#
# # fig = sns.regplot(x=x_train, y=y_train, data=df, logistic=True, ci=None)
# # fig.scatter()
# # import plotly.express as px
# # fig = px.scatter(x=x_train, y=y_train)
# # fig.show()
#
# # To predict and evaluate, you need to uncomment and use the classifier
# # y_pred = classifier.predict(x_test)
# # Evaluate the model...
#
#
# # scaler = preprocessing.StandardScaler().fit(x_train)
# # x_train = sc.fit_transform(x_train)
# # x_test = sc.transform(x_test)
# # print(x_value)
# # print(y_value)
#
#
# df.sort_index(key=lambda x1: int(x1).)
# df = df.reindex(sorted(df.columns[1:], key=lambda x: int(x.split('_')[-1][1:])), axis=1)
# x = x
#
# # print(y_values)
# print(x)
# print(y)
#
#
# df = df.T

# .to_numpy().reshape(-1, 1))
