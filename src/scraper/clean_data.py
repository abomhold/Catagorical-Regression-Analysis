import pickle
import time

import pandas as pd
import re

from bs4 import BeautifulSoup


def remove_errors(data):
    # Remove courses from the dataset that contain a specific error pattern.
    # Searches for courses with an error message matching the pattern '.*Course.*'.
    # Uses a regular expression to identify these error messages.
    # Iterates through the dataset and deletes courses that match the criteria.
    courses_to_remove = [course for course in data if re.search('.*Course.*', str(data[course]['error']))]
    for course in courses_to_remove:
        print(f'REMOVING COURSE: {course}')
        del data[course]
    return data


def remove_options(data):
    # Remove the 'options' key from the 'prereq_graph' of each course.
    # Iterates through the dataset and checks if 'prereq_graph' exists for each course.
    # If 'prereq_graph' is present, deletes the 'options' key from it.
    for course in data:
        if data[course]['prereq_graph'] is not None:
            print(f'REMOVING FOR COURSE: {course}')
            del data[course]['prereq_graph']['x']['options']
    return data


def get_totals(data):
    # Calculate the total count of grades and the overall GPA across all courses.
    # Iterates through each course's 'gpa_distro' and aggregates counts and GPA values.
    # The overall GPA is calculated as the weighted average of all GPAs.
    # If there are no grades (total_count is 0), the overall GPA is set to 0.
    total_count = sum(entry['count'] for course in data for entry in data[course]['gpa_distro'])
    total_gpa = sum(entry['count'] * int(entry['gpa']) for course in data for entry in data[course]['gpa_distro'])
    overall_gpa = total_gpa / total_count if total_count else 0
    return {"total_count": total_count, "overall_gpa": overall_gpa}


def get_gpa_courses(data):
    # Remove courses from the dataset based on their GPA distribution.
    # Identifies courses where the 9th index (assumed to be 'gpa_distro') is empty or has a total count of 0.
    # Iterates through the dataset and deletes such courses.
    # Also, prints the course identifier for each course removed.
    courses_to_remove = [course for course in data if not data[course].iloc[9] or
                         sum(grade['count'] for grade in data[course].iloc[9]) == 0]
    for course in courses_to_remove:
        print(f'REMOVING COURSE: {course}')
        del data[course]
    return data


def average(data):
    # Calculate the average GPA for each course based on 'gpa_distro' and store it in 'gpa_avg'.
    # 'gpa_distro' is assumed to be a list of dictionaries with 'count' and 'gpa' keys.
    # The function computes the weighted sum of GPAs divided by the total number of counts.
    # If 'gpa_distro' is empty, the average is set to 0.
    data['gpa_avg'] = data['gpa_distro'].apply(
        lambda distro: sum(grade['count'] * int(grade['gpa']) for grade in distro) / sum(
            grade['count'] for grade in distro) if distro else 0)
    return data


def average_no_zero(data):
    # Similar to the 'average' function but excludes zero grades ('gpa' is '0').
    # Calculates the average GPA without considering zero grades and stores it in 'gpa_avg_no_drops'.
    # If 'gpa_distro' is empty or all grades are zero, the average is set to 0.
    data['gpa_avg_no_drops'] = data['gpa_distro'].apply(
        lambda distro: sum(grade['count'] * int(grade['gpa']) for grade in distro if grade['gpa'] != '0') / sum(
            grade['count'] for grade in distro if grade['gpa'] != '0') if distro else 0)
    return data


def percent_mastered(data):
    # Calculate the percentage of grades considered as 'mastered' (where 'gpa' is 30 or higher).
    # Adds a new column 'percent_mastered' to the DataFrame showing this percentage.
    # The percentage is the count of 'mastered' grades divided by the total grade count.
    # If 'gpa_distro' is empty, the percentage is set to 0.
    data['percent_mastered'] = data['gpa_distro'].apply(
        lambda distro: sum(grade['count'] for grade in distro if int(grade['gpa']) >= 30) / sum(
            grade['count'] for grade in distro) if distro else 0)
    return data


def add_level(data):
    # Extract the course level from the last three characters of 'course_id' and add to a new column.
    # Assumes that 'course_id' ends with a three-digit number representing the course level.
    # The course level is rounded down to the nearest hundred.
    data['course_level'] = data['course_id'].apply(lambda x: int(int(x[-3:]) / 100) * 100)
    return data


def flatten_coi_data(data):
    # Extract and flatten 'coi_data' from each row into separate columns.
    # Initializes lists to store data for new columns: 'course_coi', 'course_level_coi', 'curric_coi',
    # 'percent_in_range'.
    # Iterates through the DataFrame, extracting data from 'coi_data' and appending it to the respective lists.
    # Appends None if 'coi_data' is missing or the key does not exist in 'coi_data'.
    # The new columns are added to the DataFrame with the extracted data.
    course_coi, course_level_coi, curric_coi, percent_in_range = [], [], [], []
    for index, row in data.iterrows():
        coi_data = row.get('coi_data', {})
        course_coi.append(coi_data.get('course_coi'))
        course_level_coi.append(coi_data.get('course_level_coi'))
        curric_coi.append(coi_data.get('curric_coi'))
        percent_in_range.append(coi_data.get('percent_in_range'))
    data['course_coi'], data['course_level_coi'], data['curric_coi'], data[
        'percent_in_range'] = course_coi, course_level_coi, curric_coi, percent_in_range
    return data


def flatten_concurrent_courses(data):
    # Process 'concurrent_courses' data for each row, creating a set of course keys with spaces removed.
    # Adds a new column 'concurrent_courses' to the DataFrame with the processed data.
    # If 'concurrent_courses' is missing or empty, None is appended to the list.
    courses = []
    for index, row in data.iterrows():
        concurrent_courses = row.get('concurrent_courses')
        if concurrent_courses:
            fixed_set = {key.replace(' ', '') for key in concurrent_courses.keys()}
            courses.append(fixed_set)
        else:
            courses.append(None)
    data['concurrent_courses'] = courses
    return data


def flatten_prereq(data):
    # Process prerequisite data ('prereq_graph') for each row and add two new columns: 'has_prereq' and 'is_prereq'.
    # 'has_prereq' lists courses that are prerequisites for the current course.
    # 'is_prereq' lists courses for which the current course is a prerequisite.
    # Excludes the current course ('course_id') from both lists.
    # Adds None to the lists if 'prereq_graph' is missing or does not contain the required keys.
    has_prereq_of, is_prereq_for = [], []
    for index, row in data.iterrows():
        prereq_graph = row.get('prereq_graph')
        self_course_id = row.get('course_id')
        has_set = {course.replace(' ', '') for course in
                   prereq_graph.get('x', {}).get('edges', {}).get('from', {}).values() if
                   course != self_course_id} if prereq_graph else {None}
        is_set = {course.replace(' ', '') for course in
                  prereq_graph.get('x', {}).get('edges', {}).get('to', {}).values() if
                  course != self_course_id} if prereq_graph else {None}
        has_prereq_of.append(has_set)
        is_prereq_for.append(is_set)
    data['has_prereq'], data['is_prereq'] = has_prereq_of, is_prereq_for
    return data


def flatten_course_offered(data):
    # Process 'course_offered' data for each row, extracting the quarters in which the course is offered.
    # Adds a new column 'course_offered' to the DataFrame with a set of quarters for each course.
    # Handles special cases like 'jointly' offered courses and splits on ';'.
    # Adds None if 'course_offered' is missing or no specific quarter information is found.
    offered, quarter_mapping = [], {'A': 'autumn', 'W': 'winter', 'Sp': 'spring', 'S': 'summer'}
    for index in data.index:
        line = data.loc[index]['course_offered']
        quarter_set = set()
        if line:
            if 'jointly' in line:
                line = line.split(';')[1].strip() if ';' in line else ''
            for abbrev in quarter_mapping:
                if abbrev in line:
                    quarter_set.add(quarter_mapping[abbrev])
            if not line:
                quarter_set.add(None)
        else:
            quarter_set.add(None)
        offered.append(quarter_set)
    data['course_offered'] = offered
    return data


def flatten_description(data):
    # Process 'course_description' for each row, removing prepositions, short words, and numeric words.
    # Adds a new column 'course_description' to the DataFrame with the cleaned description.
    # Splits the description into words and filters them based on specified criteria.
    # Adds a set of None if 'course_description' is missing or no words meet the criteria.
    prepositions = {'aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'among', 'around', 'before',
                    'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'concerning', 'considering', 'despite',
                    'during', 'except', 'inside', 'outside', 'regarding', 'round', 'since', 'through', 'toward',
                    'under', 'underneath', 'until', 'within', 'without'}
    for course in data.index:
        course_description = data.loc[course, 'course_description']
        if course_description:
            words = (course_description.replace(',', '').replace('.', '').replace(';', '').replace(':', '').
                     replace('/', ' ').replace(')', '').replace('(', '').split())
            string_set = {word for word in words if
                          word.lower() not in prepositions and len(word) > 4 and not word.isdigit()}
        else:
            string_set = {None}
        data.at[course, 'course_description'] = string_set
    return data


def get_department_dict():
    # Load a dictionary mapping departments to HTML data from a pickle file.
    # Process the HTML data using BeautifulSoup to extract department names.
    # Skips 'UW TACOMA' and 'UW BOTHELL' strings and any empty strings.
    # Returns a dictionary mapping department abbreviations to department names.
    with open('../clean/files/department_html_dict.pkl', 'rb') as handle:
        html_dict = pickle.load(handle)
    dep_word_list = {}
    for department in html_dict:
        soup = BeautifulSoup(str(html_dict[department]), 'html.parser')
        dep_string = soup.h1.text.split('\n')
        dep_words = [string for string in dep_string if string not in ('UW TACOMA', 'UW BOTHELL', '')]
        dep_word_list[department] = dep_words
    return dep_word_list


def add_departments(data):
    # Add a new column 'departments' to the DataFrame, mapping each course to its department(s).
    # Uses a pre-loaded department dictionary to find department names for each course.
    # Handles cases where the department abbreviation is not found in the dictionary.
    dep_dict = get_department_dict()
    dep_list = []
    for course in data.index:
        key = str(data.loc[course, 'department_abbrev']).replace(' ', '')
        dep_list.append(set(dep_dict.get(key, {None})))
    data['departments'] = dep_list
    return data


def remove_extra_columns(data):
    # Remove specific columns from the DataFrame that are no longer needed.
    # Targets columns: 'coi_data', 'gpa_distro', 'prereq_graph', 'prereq_string'.
    # Checks if each column exists before attempting to delete it.
    for column in ['coi_data', 'gpa_distro', 'prereq_graph', 'prereq_string']:
        if column in data.columns:
            del data[column]
    return data


# Initialize a dictionary to store execution times and number of entries
timings = {}
entries = {}
# Timing the data loading
start_time = time.time()
data = pd.read_json('./files/all_raw.json')  # FILE_SIZE: 27.58 MB
entries['initial'] = data.columns.size
timings['Load Data'] = time.time() - start_time
print(data)
for entry in entries:
    print(f'{entry}: {entries[entry]}')
for entry in timings:
    print(f'{entry}: {timings[entry]}')
# Timing remove_errors function
start_time = time.time()
data = remove_errors(data)
entries['Remove Errors'] = data.columns.size
timings['Remove Errors'] = time.time() - start_time
print(data)
for entry in entries:
    print(f'{entry}: {entries[entry]}')
for entry in timings:
    print(f'{entry}: {timings[entry]}')
# Timing get_gpa_courses function
start_time = time.time()
data = get_gpa_courses(data)
entries['Get GPA Courses'] = data.columns.size
timings['Get GPA Courses'] = time.time() - start_time

print(data)
for entry in entries:
    print(f'{entry}: {entries[entry]}')
for entry in timings:
    print(f'{entry}: {timings[entry]}')
v
# Timing the save to disk operation
start_time = time.time()
data.to_pickle('./files/no_gpa_dataframe.pkl')  # FILE_SIZE: 18.62 MB
timings['Save to Disk'] = time.time() - start_time

# # Timing get_totals function
# start_time = time.time()
# totals = get_totals(data)
# timings['Get Totals'] = time.time() - start_time
#
# print(totals)
#
# # Timing the load from disk operation
# start_time = time.time()
# data = pd.read_pickle('./files/no_gpa_dataframe.pkl')
# timings['Load from Disk'] = time.time() - start_time
#
# print(data)
#
# # Timing subsequent operations
# functions_to_time = [
#     ('Remove Options', remove_options),
#     ('Drop Error Column', lambda d: d.drop('error')),
#     ('Transpose Data', lambda d: d.T),
#     ('Add Departments', add_departments),
#     ('Average No Zero', average_no_zero),
#     ('Percent Mastered', percent_mastered),
#     ('Flatten COI Data', flatten_coi_data),
#     ('Flatten Concurrent Courses', flatten_concurrent_courses),
#     ('Flatten Prerequisites', flatten_prereq),
#     ('Add Level', add_level),
#     ('Flatten Course Offered', flatten_course_offered),
#     ('Flatten Description', flatten_description),
#     ('Remove Extra Columns', remove_extra_columns)
# ]
#
# for func_name, func in functions_to_time:
#     start_time = time.time()
#     data = func(data)
#     entries['initial'] = data.columns.size
#     timings[func_name] = time.time() - start_time
#     print(data.loc['TMATH208'])
#
# # Timing the final save to disk operation
# start_time = time.time()
# data.to_pickle('./files/clean_dataframe.pkl')
# timings['Final Save to Disk'] = time.time() - start_time
#
# print(data)
# print('FINAL COURSE EXAMPLE: ')
# print(data.loc['TMATH208'])
#
# # Display timings
# for operation, time_taken in timings.items():
#     print(f"{operation}: {time_taken:.2f} seconds")
