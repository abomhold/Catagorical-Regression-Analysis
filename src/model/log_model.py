import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import math
import matplotlib.pyplot as plt

# Load and prepare the data
df = pd.read_pickle('./files/clean_dataframe.pkl')

# Handle NaN values in the additional columns
df['course_coi'].fillna(df['course_coi'].mean(), inplace=True)
df['course_level_coi'].fillna(df['course_level_coi'].mean(), inplace=True)
df['curric_coi'].fillna(df['curric_coi'].mean(), inplace=True)
df['percent_in_range'].fillna(df['percent_in_range'].mean(), inplace=True)

# Process 'course_credits' - extract the lowest value and convert to int
df['course_credits'] = df['course_credits'].str.extract('(\d+\.?\d*)').astype(float)

# One-hot encode 'course_campus' and drop one category to avoid multicollinearity
campus_dummies = pd.get_dummies(df['course_campus'], drop_first=True)

# Combine all features
x = pd.concat([df[['is_bottleneck', 'is_gateway', 'course_level', 'course_coi', 'course_level_coi', 'curric_coi',
                   'percent_in_range', 'course_credits']], campus_dummies], axis=1)
x = x.astype({'is_bottleneck': bool, 'is_gateway': bool, 'course_level': int, 'course_credits': int})

# Prepare target variable y
y = df['gpa_avg'] * 1000  # Assuming gpa_avg needs to be scaled up by 1000

# Splitting data into training and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

# Instantiate and fit the model
pipeline = make_pipeline(StandardScaler(), LinearRegression())
pipeline.fit(x_train, y_train)

# Make predictions
y_pred = pipeline.predict(x_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
rmse = math.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Output the evaluation metrics
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Coefficient of Determination (R² score): {r2:.2f}")

# Extract and print model coefficients with explanations
model = pipeline.named_steps['linearregression']
coefficients = model.coef_
features = x.columns

# Combining test set and predictions for plotting
predicted_gpa = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
predicted_gpa = pd.concat([x_test.reset_index(drop=True), predicted_gpa.reset_index(drop=True)], axis=1)

print("\nModel Coefficients and their Impact on Predicted GPA:")
for feature, coef in zip(features, coefficients):
    if feature in ['is_bottleneck', 'is_gateway', 'course_level', 'course_coi', 'course_level_coi', 'curric_coi',
                   'percent_in_range', 'course_credits']:
        print(
            f"{feature}: {coef:.4f} - A unit increase in '{feature}' is associated with a change of about {coef / 1000:.3f} in GPA.")
    else:
        # For campus features
        print(
            f"{feature}: {coef:.4f} - Being in '{feature}' campus is associated with a change of about {coef / 1000:.3f} in GPA.")

# Plotting
for feature in ['tacoma', 'seattle', 'is_bottleneck', 'is_gateway', 'course_level', 'course_credits']:
    feature_avg = predicted_gpa.groupby(feature).mean()
    plt.figure()
    feature_avg['Predicted'].plot(kind='bar')
    plt.ylabel('Predicted GPA (x1000)')
    plt.title(f'Predicted GPA Average by {feature}')
    plt.xticks(rotation=45)
    plt.ylim(30000, 40000)
    plt.show()

# Mean Squared Error (MSE): 8587767.74
#
# MSE is the average of the squares of the errors between the predicted and actual values. It's a measure of the quality of the estimator. A lower MSE indicates a better fit of the model to the data. In your case, an MSE of around 8.59 million (considering your target variable gpa_avg is scaled up by 1000) is relatively high, suggesting that the model’s predictions deviate significantly from the actual values.
# Root Mean Squared Error (RMSE): 2930.49
#
# RMSE is the square root of MSE and provides a measure of the average error magnitude in the same units as the response variable. An RMSE of 2930.49, in the context of GPA scores multiplied by 1000, implies that the typical error in the predictions is about 2.930 on a 0-4 GPA scale. This is a substantial error considering the range of GPA scores.
# Mean Absolute Error (MAE): 2343.72
#
# MAE is the average of the absolute differences between the predicted values and actual values. It provides a straightforward interpretation of the average error magnitude. An MAE of 2343.72 indicates that, on average, the model’s predictions are off by about 2.344 GPA points (after scaling down by 1000).
# Coefficient of Determination (R² score): 0.13
#
# The R² score ranges from 0 to 1 and represents the proportion of the variance in the dependent variable that is predictable from the independent variables. An R² of 0.13 suggests that only 13% of the variability in GPA scores is explained by your model. This indicates a relatively weak fit of the model to your data.
# Model Coefficients:
#
#     is_bottleneck: 14.2663: This coefficient suggests that being a bottleneck course is associated with an increase of about 0.014 in GPA (when scaled back to the original GPA scale).
#     is_gateway: -242.7160: This implies that being a gateway course is associated with a decrease of about 0.243 in GPA.
#     course_level: 553.2763: For each unit increase in course level (assuming the levels are 100, 200, 300, 400), there is an associated increase of about 0.553 in GPA.
#     Campus Coefficients (bothell, seattle, tacoma): These extremely large coefficients are unusual and suggest an issue in the model. Such large values can arise from multicollinearity (high correlation between predictor variables), lack of data normalization, or other data issues. They are not meaningful in this form and indicate a potential problem with the model or data.
#
# Interpretation and Considerations:
#
#     The model's predictive accuracy is not very high, given the large MSE, RMSE, MAE, and low R².
#     The coefficients for is_bottleneck, is_gateway, and course_level provide some insights but should be interpreted cautiously given the overall model performance.
#     The exceedingly large coefficients for campuses are a red flag, indicating potential issues with the data or model specification. It's advisable to investigate the data preprocessing steps, check for multicollinearity, and ensure proper scaling and encoding of variables.
#     Consider exploring other modeling techniques or additional relevant features that could improve the model's performance.
#
