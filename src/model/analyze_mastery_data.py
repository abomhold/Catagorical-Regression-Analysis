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

# Fill NaN values with the mean of each column
df['course_coi'].fillna(df['course_coi'].mean(), inplace=True)
df['course_level_coi'].fillna(df['course_level_coi'].mean(), inplace=True)
df['curric_coi'].fillna(df['curric_coi'].mean(), inplace=True)
df['percent_in_range'].fillna(df['percent_in_range'].mean(), inplace=True)

# Extract and convert 'course_credits' to float
df['course_credits'] = df['course_credits'].str.extract('(\d+\.?\d*)').astype(float)
df['course_title'] = df['course_title'].apply(lambda title: ' '.join([word for word in title.split() if len(word) > 4]))


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

df['is_stem'] = df['departments'].apply(lambda depts: any(dept in stem_departments for dept in depts))

humanities_departments = {
    'CLASSICS', 'ENGLISH', 'HISTORY', 'PHILOSOPHY', 'ART', 'DRAMA',
    'FRENCH AND ITALIAN STUDIES', 'SCANDINAVIAN STUDIES', 'ASIAN LANGUAGES AND LITERATURE',
    'SPANISH AND PORTUGUESE STUDIES', 'COMPARATIVE HISTORY OF IDEAS', 'AMERICAN ETHNIC STUDIES',
    'GENDER, WOMEN, AND SEXUALITY STUDIES', 'AMERICAN STUDIES', 'CINEMA AND MEDIA STUDIES',
    'MUSIC', 'ART, ART HISTORY, AND DESIGN', 'RELIGION (TACOMA)', 'LITERATURE (TACOMA)',
    'ETHNIC, GENDER, AND LABOR STUDIES', 'LATIN', 'SLAVIC LANGUAGES & LITERATURES', 'GREEK',
    'BIBLICAL HEBREW', 'MODERN HEBREW', 'EGYPTIAN', 'CHINESE - TACOMA', 'JAPANESE - BOTHELL',
    'KOREAN', 'VIETNAMESE', 'URDU', 'INDONESIAN', 'TAGALOG', 'BENGALI', 'HINDI', 'THAI', 'SWAHILI'
    # Add more departments as needed
}

df['is_humanities'] = df['departments'].apply(lambda depts: any(dept in humanities_departments for dept in depts))


def get_mode_course_level(course_set):
    if not course_set or None in course_set:
        return None  # Or any default value you prefer

    # Extract course levels
    levels = [int(course[-3]) * 100 for course in course_set if len(course) >= 3]

    if not levels:
        return None  # Handle case where no valid levels are found

    # Find the mode of the levels
    level_counts = Counter(levels)
    mode_level = level_counts.most_common(1)[0][0]
    return mode_level


# Assuming df is your DataFrame and 'concurrent_courses' is the column
df['mode_concur_level'] = df['concurrent_courses'].apply(get_mode_course_level)
avg_mode_concor = int(df['mode_concur_level'].mean() / 100) * 100
# df['mode_concur_level'] = df['mode_concur_level'].apply(lambda x: avg_mode_concor if x is None or else x)
df['mode_concur_level'].fillna(int(df['mode_concur_level'].mean() / 100) * 100, inplace=True)


def extract_course_level(course_id):
    # Extract the third digit from the right and convert it to int
    try:
        return int(course_id[-3]) * 100
    except:
        return None


def calculate_mean_level(concurrent_courses):
    if not concurrent_courses or None in concurrent_courses:
        return None
    levels = [extract_course_level(course) for course in concurrent_courses]
    levels = [level for level in levels if level is not None]  # Filter out None values
    if not levels:
        return None
    mean_level = round(sum(levels) / len(levels), -2)  # Round to nearest 100
    return mean_level


# Apply the function to each row in the DataFrame
df['mean_concur_level'] = df['concurrent_courses'].apply(calculate_mean_level)
df['mean_concur_level'].fillna(int(df['mean_concur_level'].mean() / 100) * 100, inplace=True)

seasons = set.union(*df['course_offered'])

for season in seasons:
    df[f'offered_{season}'] = df['course_offered'].apply(lambda x: season in x)

df['has_prereq'] = df['has_prereq'].apply(lambda x: None not in x)
# df['is_prereq'] = df['is_prereq'].apply(lambda x: None not in x)
#
# prereqs = set.union(*df['departments'])
# print(prereqs)
# print(len(prereqs))

# for prereq in prereqs:
#     df[f'prereq_{prereq}'] = df['has_prereq'].apply(lambda x: season in x)
#
df['course_title'] = df['course_title'].apply(lambda title: {word for word in title.split() if len(word) > 4})
# df['departments_words'] = df['departments'].apply(
#     lambda title: {word for word in " ".join(str(title)).split(" ") if len(word) > 4} if None not in title else {None}

# df['departments_words'] = df['departments'].apply(lambda title: {word for word in " ".join(title).split(" ") if len(word) > 4})
#

# # print(prereq)
# for d in df.index:
#     print(df.loc[d]['departments'])

for d in df.columns:
    print(d)
print(df.loc['TMATH208'])

# def process_department(department_set):
#     excluded_words = {'TACOMA', 'BOTHELL', 'SEATTLE', 'CAMPUS', 'UWT', 'UWB'}
#     words_set = set()
#     for dept in department_set:
#         if dept is not None:
#             # Split the department string into words and filter
#             words = {word for word in dept.split() if len(word) > 4 and word not in excluded_words}
#             words_set.update(words)
#     return words_set
#
# # Apply the function to the 'departments' column
# df['departments_words'] = df['departments'].apply(process_department)

all_words = [word for description in df['course_description'] for word in description]
all_words += [word for description in df['course_title'] for word in description]
# all_words += [word for description in df['departments_words'] for word in description]
# Count the frequency of each word

word_counts = Counter(all_words)

# Identify the top 10 most frequent words
top_10_words = [word for word, count in word_counts.most_common(250)]

# Create new columns for each of the top 10 words
# for word in top_10_words:
#     column_name = f"word_{word}"
#     df[column_name] = df['course_description'].apply(lambda desc: word in desc)
#
# print(top_10_words)

##################################################################################################
# One-hot encode 'course_campus' and drop one category to avoid multicollinearity
campus_dummies = pd.get_dummies(df['course_campus'], drop_first=True)
# = pd.get_dummies(df['department_abbrev'], drop_first=True)

# Combine all features for the model

# Start with the existing columns in x
x = df[['is_bottleneck', 'is_gateway', 'course_level', 'course_credits', 'offered_winter', 'offered_summer', 'offered_spring',
        'offered_autumn', 'has_prereq', 'is_stem', 'is_humanities', 'mean_concur_level']].copy()

# 'course_coi', 'course_level_coi', 'curric_coi','percent_in_range',

# Assuming 'top_10_words' is a list of words you want to add as columns
top_10_word_columns = {}

for word in top_10_words:
    column_name = f"word_{word}"
    top_10_word_columns[column_name] = df.apply(lambda row: word in row['course_description'] or word in row['course_title'], axis=1)

# Create a new DataFrame from the dictionary
new_columns_df = pd.DataFrame(top_10_word_columns)

# Concatenate this with your existing DataFrame
x = pd.concat([x, new_columns_df], axis=1)
# Add new columns for each of the top 10 words
# for word in top_10_words:
#     column_name = f"word_{word}"
#     x[column_name] = df.apply(lambda row: word in row['course_description'] or word in row['course_title'], axis=1).copy()
    # x[column_name] = df['course_description'].apply(lambda desc: word in desc).copy()
#or word in row['departments_words']
# Concatenate with campus dummies
x = pd.concat([x, campus_dummies], axis=1)
# x = pd.concat([df[['is_bottleneck', 'is_gateway', 'course_level', 'course_coi', 'course_level_coi', 'curric_coi',
#                    'percent_in_range', 'course_credits', 'offered_winter', 'offered_summer', 'offered_spring',
#                    'offered_autumn', 'has_prereq', 'is_stem', 'is_humanities', 'mean_concur_level']] +
#                [df[f"word_{word}"] for word in top_10_words] +
#                [campus_dummies]], axis=1)
# # x = pd.concat([df[['is_bottleneck', 'is_gateway', 'course_level', 'course_coi', 'course_level_coi', 'curric_coi',
# #                    'percent_in_range', 'course_credits', 'offered_winter', 'offered_summer', 'offered_spring',
# #                    'offered_autumn', 'has_prereq', 'is_stem', 'is_humanities', 'mean_concur_level']],
# #                campus_dummies], axis=1)
x = x.astype({'is_bottleneck': bool, 'is_gateway': bool, 'course_level': int, 'course_credits': int})

# Prepare target variable y by scaling the GPA
#y = df['gpa_avg_no_drops'] # / 100
y = df['percent_mastered']  # / 100
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
    # Skip features with coefficients between -0.005 and 0.005
    if -0.0005 < coef < 0.0005:
        continue

    # Skip specified features
    # if feature in ['course_coi', 'course_level_coi', 'curric_coi', 'percent_in_range']:
    #     continue

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
# # Print sorted feature impacts
# print("\nSorted Model Coefficients and their Impact (as Percentage):")
# for feature, change in feature_impact:
#     print(f"{feature}: {change:.2f}%")
#
# # # for feature, coef in zip(features, coefficients):
# # #     print(f"{feature}: {coef:.4f}")
# # print("\nModel Coefficients and their Impact on Predicted GPA (as Percentage):")
# # for feature, coef in zip(features, coefficients):
# #     # Skip features whose coefficients are between -0.005 and 0.005
# #     if -0.005 < coef < 0.005:
# #         continue
# #
# #     # # Skip specified features
# #     # if feature in ['course_coi', 'course_level_coi', 'curric_coi', 'percent_in_range']:
# #     #     continue
# #
# #     # For boolean features
# #     if feature in ['is_bottleneck', 'is_gateway']:
# #         print(
# #             f"{feature}: {coef:.4f} - If '{feature}' is true, it is associated with a {coef * 100:.2f}% change in competency.")
# #
# #     # For other features, assuming they are words
# #     else:
# #         print(
# #             f"{feature}: {coef:.4f} - The presence of '{feature}' is associated with a {coef * 100:.2f}% change in competency.")
# # # Print out the coefficients with their meanings
# # print("\nModel Coefficients and their Impact on Predicted GPA (as Percentage):")
# # for feature, coef in zip(features, coefficients):
# #     if feature == 'is_bottleneck':
# #         print(
# #             f"{feature}: {coef:.4f} - Being a bottleneck course (if True) is associated with a {coef:.2f}% change in competency.")
# #     elif feature == 'is_gateway':
# #         print(
# #             f"{feature}: {coef:.4f} - Being a gateway course (if True) is associated with a {coef:.2f}% change in competency.")
# #     elif feature not in ['course_coi', 'course_level_coi', 'curric_coi', 'percent_in_range']:
# #         print(
# #             f"{feature}: {coef:.4f} - A unit increase in '{feature}' is associated with a {coef:.2f}% change in competency.")

# Combine test set and predictions for plotting
predicted_gpa = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
predicted_gpa = pd.concat([x_test.reset_index(drop=True), predicted_gpa.reset_index(drop=True)], axis=1)

# Plotting
for feature in ['tacoma', 'seattle', 'is_bottleneck', 'is_gateway', 'course_level', 'course_credits', 'has_prereq','mean_concur_level']:
    feature_avg = predicted_gpa.groupby(feature).mean()
    plt.figure()
    feature_avg['Predicted'].plot(kind='bar')
    plt.ylabel('Predicted Percent >= 3.0')
    plt.title(f'Predicted Percent >= 3.0 by {feature}')
    plt.xticks(rotation=45)
    # plt.ylim(30000, 40000)
    plt.ylim(0.7, 1.0)
    plt.show()
