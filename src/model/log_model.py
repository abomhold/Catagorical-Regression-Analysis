import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
import math

# Load and prepare the data
df = pd.read_pickle('./files/clean_dataframe.pkl')
df.reset_index(names=['courses'], inplace=True)

# Prepare feature matrix X
# Convert 'course_campus' to dummy variables
dummies_campus = pd.get_dummies(df['course_campus'])

# Combine all features
x = pd.concat([df[['is_bottleneck', 'is_gateway', 'course_level']], dummies_campus], axis='columns')
x = x.astype(
    {'is_bottleneck': bool, 'is_gateway': bool, 'course_level': int, 'bothell': bool, 'seattle': bool, 'tacoma': bool})

# Prepare target variable y
y = df[['gpa_avg']].copy()
y['gpa_avg'] = df.gpa_avg.multiply(1000).round().astype(int)
y = y.gpa_avg

# Splitting data into training and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

# Instantiate Standard Scaler and Linear Regression
scaler = StandardScaler()
regressor = LinearRegression()

# Creating a pipeline
pipeline = Pipeline([('scaler', scaler), ('regressor', regressor)])
pipeline.fit(x_train, y_train)

# Make predictions
y_pred = pipeline.predict(x_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
rmse = math.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Coefficient of Determination (R² score): {r2:.2f}")

# Combine test set and predictions for plotting
predicted_gpa = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
predicted_gpa = pd.concat([x_test.reset_index(drop=True), predicted_gpa.reset_index(drop=True)], axis=1)

# Plotting the bar plot for predicted GPA averages for each feature
for feature in ['bothell', 'seattle', 'tacoma', 'is_bottleneck', 'is_gateway', 'course_level']:
    feature_avg = predicted_gpa.groupby(feature).mean()
    plt.figure()
    feature_avg['Predicted'].plot(kind='bar')
    plt.ylabel('Predicted GPA (x1000)')
    plt.title(f'Predicted GPA Average by {feature}')
    plt.ylim(33000, 37000)
    plt.show()
