import pandas as pd
df = pd.read_pickle('./files/clean_dataframe.pkl')
print(df.loc['TMATH208'])
# for index in df.index:
#     print(f'{index}\n{df.loc[index]['course_description']}')

# Assuming the target variable is in the first column
# y = df.iloc[:, 13]
#
# x = df.iloc[:, 14:]
# print(y)
# print(x)
# # Splitting data into training and test.json sets
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
#
# # Data preprocessing
# scaler = StandardScaler()
# x_train = scaler.fit_transform(x_train)
# x_test = scaler.transform(x_test)
#
# # PCA for dimensionality reduction
# pca = PCA(n_components=1)
# x_train = pca.fit_transform(x_train)
# x_test = pca.transform(x_test)
# explained_variance = pca.explained_variance_ratio_
# print(explained_variance)
