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
df = pd.read_pickle('files/clean_dataframe.pkl')

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

new_columns_df = get_words(100)
campus_dummies = pd.get_dummies(df['course_campus'], drop_first=True)

# Combine all features for the model
# Assign X
x = df[['is_bottleneck', 'is_gateway', 'course_level', 'course_credits', 'offered_winter', 'offered_summer',
        'offered_spring', 'offered_autumn', 'has_prereq', 'is_stem', 'is_humanities', 'mean_concur_level', 'course_coi', 'course_level_coi', 'curric_coi', 'percent_in_range']].copy()
x = pd.concat([x, campus_dummies, new_columns_df], axis=1)
# Assign Y
y = df['percent_mastered']
# y = df['gpa_avg']
#######################################################################################################################

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
feature_impact = [(feature, coef * 100) for feature, coef in zip(features, coefficients)]

# Sort the list by the absolute value of percent change, in descending order
feature_impact.sort(key=lambda x: abs(x[1]), reverse=True)

# Define groups of features
campus_features = ['seattle', 'tacoma']
season_features = ['offered_winter', 'offered_summer', 'offered_spring', 'offered_autumn']
bottleneck_gateway_features = ['is_bottleneck', 'is_gateway','has_prereq']
course_level_features = ['course_level', 'mean_concur_level']
discipline_features = ['is_humanities', 'is_stem']
word_features = [f for f, _ in feature_impact if f.startswith("word_")]


# Function to print feature impacts
def print_feature_impacts(group, title):
    print(f"\n{title}:")
    for feature in group:
        change = next((change for f, change in feature_impact if f == feature), None)
        if change is not None:
            print(f"  {feature}: {change:.2f}%")


# Print impacts of different feature groups
print_feature_impacts(campus_features, "Campus Features")
print_feature_impacts(season_features, "Season Features")
print_feature_impacts(bottleneck_gateway_features, "Bottleneck and Gateway Features")
print_feature_impacts(course_level_features, "Course Level Features")
print_feature_impacts(discipline_features, "Discipline Features")

# Separate section for word features
print("\nTop Ten 'word_' Features and their Impact (as Percentage):")
for feature in word_features[:25]:  # Limit to top 10
    change = next((change for f, change in feature_impact if f == feature), None)
    print(f"  {feature}: {change:.2f}%")

# Combine test set and predictions for plotting
predicted_gpa = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
predicted_gpa = pd.concat([x_test.reset_index(drop=True), predicted_gpa.reset_index(drop=True)], axis=1)


# Function to create bar graphs for binary features
# Function to plot a consolidated bar graph
def plot_grouped_bar(dataframe, features, title):
    means = {feature: dataframe.groupby(feature)['Predicted'].mean() for feature in features}
    df_means = pd.DataFrame(means)

    df_means.plot(kind='bar')
    plt.ylabel('Percentage >3.0')
    plt.title(title)
    plt.xticks(rotation=0)
    plt.legend(title="Feature")
    plt.ylim(.7, 1)
    plt.show()


def plot_boolean_bar(dataframe, features, title):
    df = dataframe.copy()
    for feature in features:
        df[feature] = df[feature].map({True: 'True', False: 'False'})

    melted_df = df.melt(value_vars=features, id_vars='Predicted', var_name='Feature', value_name='Value')
    means = melted_df.groupby(['Feature', 'Value'])['Predicted'].mean().unstack()

    means.plot(kind='bar', stacked=False)
    plt.ylabel('Percentage >3.0')
    plt.title(title)
    plt.xticks(rotation=45)
    plt.legend(title="Value")
    plt.ylim(.7, 1)
    plt.show()


# 1) Campuses: Seattle and Tacoma
plot_boolean_bar(predicted_gpa, ['seattle', 'tacoma'], 'Percentage >3.0 by Campus')

# 2) Seasons
plot_boolean_bar(predicted_gpa, ['offered_winter', 'offered_summer', 'offered_spring', 'offered_autumn'],
                 'Percentage >3.0 by Season')

# 3) Bottleneck, Gateway, and Prerequisites
plot_boolean_bar(predicted_gpa, ['is_bottleneck', 'is_gateway', 'has_prereq'],
                 'Percentage >3.0 by Course Characteristics')

# 4) Course Level and Mean Concurrent Level
plot_grouped_bar(predicted_gpa, ['course_level', 'mean_concur_level'],
                 'Percentage >3.0 by Course and Concurrent Levels')

# 5) Humanities and STEM
plot_boolean_bar(predicted_gpa, ['is_humanities', 'is_stem'], 'Percentage >3.0 by Discipline Type')

# 6) Top 10 Words

plot_boolean_bar(predicted_gpa, word_features[:10], 'Percentage >3.0 by Presence of Top 10 Words')
