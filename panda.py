from array import array

import pandas
from sklearn import preprocessing
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

gpa_dict = eval(open('grades.dict', 'r').read())
df = pd.DataFrame(gpa_dict['TCSS'])
# df.sort_index(key=lambda x1: int(x1).)
df.index = df.index.astype(int)
# df = df.reindex(sorted(df.columns[1:], key=lambda x: int(x.split('_')[-1][1:])), axis=1)

df = df.sort_index(ascending=True)
df = df.T
x = df.columns
x = x.to_numpy()
x = x.reshape(-1, 1)
y = df.T.values
print(y)
print(x)
# x = df.iloc[:, 0].values
# print(x)

x_train, x_test, y_train, y_test = train_test_split(y, x, test_size=0.2, random_state=0)
pt = preprocessing.PowerTransformer(method='yeo-johnson', standardize=False)
# x_test = pt.fit_transform(x_test)
# x_train = pt.fit_transform(x_train)
from sklearn.decomposition import PCA

pca = PCA(n_components=1)
x_train = pca.fit_transform(x_train)
x_test = pca.transform(x_test)
explained_variance = pca.explained_variance_ratio_
print(explained_variance)

# from sklearn.linear_model import LogisticRegression
#
# classifier = LogisticRegression(random_state=0)
# classifier.fit(x_train, y_train)

# scaler = preprocessing.StandardScaler().fit(x_train)
# x_train = sc.fit_transform(x_train)
# # x_test = sc.transform(x_test)
# print(x_value)
# print(y_value)

# import plotly.express as px
#
# fig = px.scatter(x=x, y=y)
# fig.show()
