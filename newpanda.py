import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import seaborn as sns
gpa_dict = eval(open('percents', 'r').read())

data = []
for course, grades in gpa_dict.items():
    for grade, count in grades.items():
        for _ in range(count):
            data.append({'course': course, 'grade': int(grade)})

df = pd.DataFrame(data)
print(df)

# X_train, X_test, y_train, y_test = train_test_split(df[['course']], df['grade'], test_size=0.2)
# model = LinearRegression()
# model.fit(X_train, y_train)

# data = []
# for dept, courses in gpa_dict.items():
#     for course, grades in courses.items():
#         for grade, count in grades.items():
#             for _ in range(count):
#                 data.append({'course': f'{dept}{course}', 'grade': int(grade)})
#
# df = pd.DataFrame(data)
# print(df)
# Create a frequency DataFrame
grade_counts = df['grade'].value_counts().sort_index().reset_index()
grade_counts.columns = ['grade', 'count']
#
# Plotting the grade distribution
plt.figure(figsize=(10, 6))
sns.barplot(x='grade', y='count', data=grade_counts)
plt.xlabel('Grade')
plt.ylabel('Frequency (Likelihood)')
plt.title('Frequency Distribution of Grades')
plt.show()