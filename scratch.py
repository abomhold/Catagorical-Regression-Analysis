import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PowerTransformer, StandardScaler
from sklearn.decomposition import PCA
# from sklearn.linear_model import LogisticRegression  # Uncomment if you want to use Logistic Regression

# Load data
gpa_dict = eval(open('grades.dict', 'r').read())
df = pd.DataFrame(gpa_dict['TCSS'])

# Convert index to integers and sort
df.index = df.index.astype(int)
df = df.sort_index(ascending=True)

# Transpose the DataFrame
df = df.T

# Assuming the target variable is in the first column
y = df.iloc[:, 0].values
x = df.iloc[:, 1:].values

# Splitting data into training and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Data preprocessing
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# PCA for dimensionality reduction
pca = PCA(n_components=1)
x_train = pca.fit_transform(x_train)
x_test = pca.transform(x_test)
explained_variance = pca.explained_variance_ratio_
print(explained_variance)

# # Uncomment below if you want to train a logistic regression model
# classifier = LogisticRegression(random_state=0)
# classifier.fit(x_train, y_train)

from sklearn.linear_model import LogisticRegression

# Increasing the maximum number of iterations and changing the solver
classifier = LogisticRegression(random_state=0, max_iter=1000, solver='lbfgs')  # You can try different solvers like 'liblinear', 'newton-cg', etc.

# Fit the model
a = classifier.fit(x_train, y_train)
print(a)
# Predict using the test set
y_pred = classifier.predict(x_test)
print(y_pred)
# Evaluate the model...
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

# Assume y_test are your true labels and y_pred are the predictions from the logistic regression model
y_pred = classifier.predict(x_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
avg ='macro'
# Precision
precision = precision_score(y_test, y_pred, average=avg)
print(f"Precision: {precision}")

# Recall
recall = recall_score(y_test, y_pred, average=avg)
print(f"Recall: {recall}")

# F1 Score
f1 = f1_score(y_test, y_pred, average=avg)
print(f"F1 Score: {f1}")

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
print(f"Confusion Matrix:\n{conf_matrix}")

# To predict and evaluate, you need to uncomment and use the classifier
# y_pred = classifier.predict(x_test)
# Evaluate the model...
