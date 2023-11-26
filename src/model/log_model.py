import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import metrics
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import seaborn as sns

df = pd.read_pickle('./files/clean_dataframe.pkl')
df.reset_index(names=['courses'], inplace=True)

x = df[['course_campus', 'is_bottleneck', 'is_gateway', 'course_level']]
dummies_campus = pd.get_dummies(x['course_campus'])
# dummies_department = pd.get_dummies(x['department_abbrev'])
x = pd.concat([x, dummies_campus], axis='columns')
x = x.drop(['course_campus'], axis='columns')
x = x.astype(
    {'is_bottleneck': bool, 'is_gateway': bool, 'course_level': int, 'bothell': bool, 'seattle': bool, 'tacoma': bool})
print(x.columns)

y = df[['gpa_avg']].copy()
y['gpa_avg'] = df.gpa_avg.multiply(1000).round().astype(int)
print(y)

# Splitting data into training and test.json sets
x_test, x_train, y_test, y_train = train_test_split(x, y.values.ravel(), test_size=0.25, random_state=0)
print(x_train, x_test, y_train, y_test)

# PCA for dimensionality reduction
pca = PCA(n_components=6)
x_train = pca.fit_transform(x_train)
x_test = pca.transform(x_test)
explained_variance = pca.explained_variance_ratio_
print(x_train, x_test)
print(explained_variance)

# import the class
from sklearn.linear_model import LogisticRegression

# instantiate the model (using the default parameters)
logreg = LogisticRegression(random_state=16, max_iter=10000)

# fit the model with data
logreg.fit(x_train, y_train)

y_pred = logreg.predict(x_test)
print(y_pred)

cnf_matrix = metrics.confusion_matrix(y_test, y_pred)

print(cnf_matrix)

class_names = list(y.columns)  # name  of classes

fig, ax = plt.subplots()

tick_marks = np.arange(len(class_names))

plt.xticks(tick_marks, 'test_x')

plt.yticks(tick_marks, 'test_y')

# create heatmap

sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu", fmt='g')

ax.xaxis.set_label_position("top")

plt.tight_layout()

plt.title('Confusion matrix', y=1.1)

plt.ylabel('Actual label')

plt.xlabel('Predicted label')

#
