import pandas as pd
import re


def remove_errors(data):
    courses_to_remove = [course for course in data if re.search('.*Course.*', str(data[course]['error']))]
    for course in courses_to_remove:
        del data[course]
    return data


def remove_options(data):
    for course in data:
        if data[course]['prereq_graph'] is not None:
            del data[course]['prereq_graph']['x']['options']
    return data


def get_totals(data):
    total_count = sum(entry['count'] for course in data for entry in data[course]['gpa_distro'])
    total_gpa = sum(entry['count'] * int(entry['gpa']) for course in data for entry in data[course]['gpa_distro'])
    overall_gpa = total_gpa / total_count if total_count else 0
    return {"total_count": total_count, "overall_gpa": overall_gpa}


def get_gpa_courses(data):
    courses_to_remove = [course for course in data if not data[course].iloc[9] or
                         sum(grade['count'] for grade in data[course].iloc[9]) == 0]
    for course in courses_to_remove:
        print(course)
        del data[course]
    return data




# data = pd.read_json('./files/all_raw.json') # FILE_SIZE: 27.58 MB
# # remove errors
# data = remove_errors(data)
# # remove courses without gpa distros
# data = get_gpa_courses(data)
# print(data)
# # save to disk time heavy operation
# data.to_pickle('./files/no_gpa_dataframe.pkl') # FILE_SIZE: 18.62 MB

data = pd.read_pickle('./files/no_gpa_dataframe.pkl')
print(data)
data = remove_options(data)
print(data)
data = data.drop('error')
print(data)
data.to_pickle('./files/formatted_dataframe.pkl')
for index in data.columns:
    print(data[index])
totals = get_totals(data)
print(totals)
