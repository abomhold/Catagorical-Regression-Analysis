from collections import Counter

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import math
import matplotlib.pyplot as plt

# Load the data
df = pd.read_pickle('./files/clean_dataframe.pkl')

stem_departments = {
    'EARTH AND SPACE SCIENCES', 'INDUSTRIAL ENGINEERING', 'PHYSICS', 'BIOLOGICAL SCIENCE (BOTHELL)',
    'GEOSCIENCES', 'ENVIRONMENTAL SCIENCE', 'INSTITUTE OF TECHNOLOGY - TACOMA', 'OCEANOGRAPHY',
    'AERONAUTICS AND ASTRONAUTICS', 'MATERIALS SCIENCE & ENGINEERING', 'CHEMISTRY - BOTHELL',
    'MATHEMATICS - TACOMA', 'FISHERIES', 'BIOLOGY - UW BOTHELL', 'AERONAUTICS & ASTRONAUTICS',
    'MECHANICAL ENGINEERING - TACOMA', 'COMPUTING & SOFTWARE SYSTEMS', 'GENOME SCIENCES',
    'SCHOOL OF OCEANOGRAPHY', 'MARINE BIOLOGY', 'STATISTICS', 'NANOSCIENCE AND MOLECULAR ENGINEERING',
    'CHEMISTRY', 'COMPUTATIONAL FINANCE & RISK MANAGEMENT', 'SCHOOL OF MARINE & ENVIRONMENTAL AFFAIRS',
    'PHYSICS - TACOMA', 'SCIENCE AND TECHNOLOGY - UW BOTHELL', 'ELECTRICAL ENGINEERING - UW BOTHELL',
    'ENGINEERING - BOTHELL', 'SCHOOL OF NURSING', 'AERONAUTICS & ASTRONAUTICS', 'COMPUTER SCIENCE & ENGINEERING',
    'SCHOOL OF ENVIRONMENTAL & FOREST SCIENCE', 'CIVIL & ENVIRONMENTAL ENGINEERING', 'ELECTRICAL ENGINEERING',
    'MATHEMATICS', 'ELECTRICAL ENGINEERING - TACOMA', 'COMPUTER ENGINEERING & SYSTEMS (TACOMA)',
    'EARTH SYSTEM SCIENCE (BOTHELL)', 'SCHOOL OF ENGINEERING & TECHNOLOGY - UWT', 'CHEMICAL ENGINEERING',
    'ELECTRICAL AND COMPUTER ENGINEERING', 'COMPUTER SCIENCE & SYSTEMS - TACOMA', 'MECHANICAL ENGINEERING - UW BOTHELL',
    'SCHOOL OF AQUATIC AND FISHERY SCIENCES', 'HUMAN CENTERED DESIGN AND ENGINEERING',
    'INDUSTRIAL AND SYSTEMS ENGINEERING',
    'COMPUTER SCIENCE AND ENGINEERING'
}

humanities_departments = {
    'CLASSICS', 'ENGLISH', 'HISTORY', 'PHILOSOPHY', 'ART', 'DRAMA',
    'FRENCH AND ITALIAN STUDIES', 'SCANDINAVIAN STUDIES', 'ASIAN LANGUAGES AND LITERATURE',
    'SPANISH AND PORTUGUESE STUDIES', 'COMPARATIVE HISTORY OF IDEAS', 'AMERICAN ETHNIC STUDIES',
    'GENDER, WOMEN, AND SEXUALITY STUDIES', 'AMERICAN STUDIES', 'CINEMA AND MEDIA STUDIES',
    'MUSIC', 'ART, ART HISTORY, AND DESIGN', 'RELIGION (TACOMA)', 'LITERATURE (TACOMA)',
    'ETHNIC, GENDER, AND LABOR STUDIES', 'LATIN', 'SLAVIC LANGUAGES & LITERATURES', 'GREEK',
    'BIBLICAL HEBREW', 'MODERN HEBREW', 'EGYPTIAN', 'CHINESE - TACOMA', 'JAPANESE - BOTHELL',
    'KOREAN', 'VIETNAMESE', 'URDU', 'INDONESIAN', 'TAGALOG', 'BENGALI', 'HINDI', 'THAI', 'SWAHILI'
}


def calculate_mean_level(concurrent_courses):
    if not concurrent_courses or None in concurrent_courses:
        return None
    levels = [int(course[-3]) * 100 for course in concurrent_courses]
    # levels = [level for level in levels if level is not None]  # Filter out None values
    mean_level = round(sum(levels) / len(levels), -2)  # Round to nearest 100
    return mean_level


def get_words(x):
    all_words = [word for description in df['course_description'] for word in description]
    all_words += [word for description in df['course_title'] for word in description]
    # Count the frequency of each word
    word_counts = Counter(all_words)
    # Identify the top 10 most frequent words
    top_words = [word for word, count in word_counts.most_common(x)]
    # Assuming 'top_10_words' is a list of words you want to add as columns
    top_word_columns = {}
    for word in top_words:
        column_name = f"word_{word}"
        top_word_columns[column_name] = df.apply(
            lambda row: word in row['course_description'] or word in row['course_title'], axis=1)
    return pd.DataFrame(top_word_columns)


# Fill NaN values with the mean of each column
df['course_coi'].fillna(df['course_coi'].mean(), inplace=True)
df['course_level_coi'].fillna(df['course_level_coi'].mean(), inplace=True)
df['curric_coi'].fillna(df['curric_coi'].mean(), inplace=True)
df['percent_in_range'].fillna(df['percent_in_range'].mean(), inplace=True)

# Extract and convert 'course_credits' to float
df['course_credits'] = df['course_credits'].str.extract('(\d+\.?\d*)').astype(float)
df['course_title'] = df['course_title'].apply(lambda title: ' '.join([word for word in title.split() if len(word) > 4]))

df['mean_concur_level'] = df['concurrent_courses'].apply(calculate_mean_level)
df['mean_concur_level'].fillna(int(df['mean_concur_level'].mean() / 100) * 100, inplace=True)

df['is_stem'] = df['departments'].apply(lambda depts: any(dept in stem_departments for dept in depts))
df['is_humanities'] = df['departments'].apply(lambda depts: any(dept in humanities_departments for dept in depts))

seasons = set.union(*df['course_offered'])
for season in seasons:
    df[f'offered_{season}'] = df['course_offered'].apply(lambda x: season in x)

df['has_prereq'] = df['has_prereq'].apply(lambda x: None not in x)
df['course_title'] = df['course_title'].apply(lambda title: {word for word in title.split() if len(word) > 4})

new_columns_df = get_words(25)
campus_dummies = pd.get_dummies(df['course_campus'], drop_first=True)


# Combine all features for the model
# Assign X
x = df[['is_bottleneck', 'is_gateway', 'course_level', 'course_credits', 'offered_winter', 'offered_summer',
        'offered_spring', 'offered_autumn', 'has_prereq', 'is_stem', 'is_humanities', 'mean_concur_level']].copy()
x = pd.concat([x, campus_dummies, new_columns_df], axis=1)
# Assign Y
y = df['percent_mastered']

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=0)

# Create a pipeline for scaling and linear regression
pipeline = make_pipeline(StandardScaler(), LinearRegression())
pipeline.fit(x_train, y_train)

# Predict using the model
y_pred = pipeline.predict(x_test)

# Evaluate the model's performance
mse = mean_squared_error(y_test, y_pred)
rmse = math.sqrt(mse)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Print out the evaluation metrics
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Coefficient of Determination (R² score): {r2:.2f}")

# Extract model coefficients
model = pipeline.named_steps['linearregression']
coefficients = model.coef_
features = x.columns

# List to store feature names and their corresponding percent change
feature_impact = []

for feature, coef in zip(features, coefficients):
    # Calculate percent change and store in the list
    percent_change = coef * 100
    feature_impact.append((feature, percent_change))

# Sort the list by the absolute value of percent change, in descending order
feature_impact.sort(key=lambda x: abs(x[1]), reverse=True)

# Assuming feature_impact is a list of tuples (feature, impact)
regular_features = []
word_features = []

# Split features into regular and word_ features
for feature, change in feature_impact:
    if feature.startswith("word_"):
        word_features.append((feature, change))
    else:
        regular_features.append((feature, change))

# Sort features based on absolute value of impact
# regular_features.sort(key=lambda x: abs(x[1]), reverse=True)
word_features.sort(key=lambda x: abs(x[1]), reverse=True)

# Print sorted regular features
print("\nSorted Model Coefficients and their Impact (as Percentage) for Regular Features:")
for feature, change in regular_features:
    print(f"{feature}: {change:.2f}%")

# Print top ten word features
print("\nTop Ten 'word_' Features and their Impact (as Percentage):")
for feature, change in word_features[:10]:  # Limit to top 10
    print(f"{feature}: {change:.2f}%")

# Combine test set and predictions for plotting
predicted_gpa = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
predicted_gpa = pd.concat([x_test.reset_index(drop=True), predicted_gpa.reset_index(drop=True)], axis=1)

# Plotting
for feature in ['tacoma', 'seattle', 'is_bottleneck', 'is_gateway', 'course_level', 'course_credits', 'has_prereq',
                'mean_concur_level']:
    feature_avg = predicted_gpa.groupby(feature).mean()
    plt.figure()
    feature_avg['Predicted'].plot(kind='bar')
    plt.ylabel('Predicted Percent >= 3.0')
    plt.title(f'Predicted Percent >= 3.0 by {feature}')
    plt.xticks(rotation=45)
    # plt.ylim(30000, 40000)
    plt.ylim(0.7, 1.0)
    plt.show()
