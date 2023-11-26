import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error

# Load and prepare the data
df = pd.read_pickle('./files/clean_dataframe.pkl')
df.reset_index(names=['courses'], inplace=True)
print(list(df.columns))
# # Prepare feature matrix X
# x = df[['course_campus']]
# dummies_campus = pd.get_dummies(x['course_campus'])
# x = pd.concat([x, dummies_campus], axis='columns')
# x = x.drop(['course_campus'], axis='columns')
# x = x.astype({'bothell': bool, 'seattle': bool, 'tacoma': bool})

# Prepare feature matrix X
x = df[['course_level']]
# dummies_level = pd.get_dummies(x['course_level'])
# x = pd.concat([x, dummies_level], axis='columns')
# x = x.drop(['course_level'], axis='columns')
x = x.astype({'course_level': int})

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
print(f"Mean Squared Error: {mse}")

# Plotting the bar plot for predicted GPA averages for each campus
predicted_gpa = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
predicted_gpa = pd.concat([x_test.reset_index(drop=True), predicted_gpa.reset_index(drop=True)], axis=1)

# Aggregate predictions by campus
level_avg = predicted_gpa.groupby([100, 200, 300, 400]).mean()

# Plot
level_avg['Predicted'].plot(kind='bar')
plt.ylabel('Predicted GPA (x1000)')
plt.title('Predicted GPA Average by Leve')
plt.xticks(ticks=[0, 1, 2, 3], labels=['100', '200', '300', '400'], rotation=0)
plt.show()
