import pickle
import pandas as pd

from bs4 import BeautifulSoup

TOTAL_COUNTS = 2370259
OVERALL_GPA = 33.675253210725074

data = pd.read_pickle('files/formatted_dataframe.pkl').T
print(data)


def average(data):
    # Assuming 'gpa_distro' is a column containing a list of dictionaries
    data['gpa_avg'] = data['gpa_distro'].apply(
        lambda distro: sum(grade['count'] * int(grade['gpa']) for grade in distro) / sum(
            grade['count'] for grade in distro) if distro else 0)
    return data


def average_no_zero(data):
    data['gpa_avg_no_drops'] = data['gpa_distro'].apply(
        lambda distro: sum(grade['count'] * int(grade['gpa']) for grade in distro if grade['gpa'] != '0') / sum(
            grade['count'] for grade in distro if grade['gpa'] != '0') if distro else 0)
    return data


def percent_mastered(data):
    data['percent_mastered'] = data['gpa_distro'].apply(
        lambda distro: sum(grade['count'] for grade in distro if int(grade['gpa']) >= 30) / sum(
            grade['count'] for grade in distro) if distro else 0)
    return data


#
# def average(data):
#     avg_list = []
#     for course in data.columns:
#         totalcount = 0
#         totalgpa = 0
#         for grade in data[course]['gpa_distro']:
#             totalcount += grade['count']
#             totalgpa += grade['count'] * int(grade['gpa'])
#         avg_list.append(totalgpa / totalcount)
#     data.loc['gpa_avg'] = avg_list
#     return data
#
#
# def average_no_zero(data):
#     avg_list = []
#     for course in data.columns:
#         totalcount = 0
#         totalgpa = 0
#         for grade in data[course]['gpa_distro']:
#             if grade['gpa'] != '0':
#                 totalcount += grade['count']
#                 totalgpa += grade['count'] * int(grade['gpa'])
#         avg_list.append(totalgpa / totalcount)
#     data.loc['gpa_avg_no_drops'] = avg_list
#     return data
#
#
# def percent_mastered(data):
#     avg_list = []
#
#     for course in data.columns:
#         gpa_distro = data[course]['gpa_distro']
#
#         total_count = sum(grade['count'] for grade in gpa_distro)
#         mastered_count = sum(grade['count'] for grade in gpa_distro if int(grade['gpa']) >= 30)
#
#         # Handle division by zero if total_count is 0
#         avg = (mastered_count / total_count) if total_count > 0 else 0
#         avg_list.append(avg)
#
#     data.loc['percent_mastered'] = avg_list
#     return data

def add_level(data):
    data['course_level'] = data['course_id'].apply(lambda x: int(int(x[-3:]) / 100) * 100)
    return data


# def add_level(data):
#     level = []
#     for course in data.columns:
#         number = int(data[course, 'course_id'][-3:])
#         level.append(int(number / 100) * 100)
#     data['course_level'] = level
#     return data


def flatten_coi_data(data):
    # Lists to hold the data for each new column
    course_coi = []
    course_level_coi = []
    curric_coi = []
    percent_in_range = []

    # Iterate over the DataFrame rows
    for index, row in data.iterrows():
        coi_data = row.get('coi_data', {})  # Use a default empty dictionary if 'coi_data' is missing

        # Extract each piece of data, using a default value if the key is missing
        course_coi.append(coi_data.get('course_coi'))
        course_level_coi.append(coi_data.get('course_level_coi'))
        curric_coi.append(coi_data.get('curric_coi'))
        percent_in_range.append(coi_data.get('percent_in_range'))

    # Add the new columns to the DataFrame
    data['course_coi'] = course_coi
    data['course_level_coi'] = course_level_coi
    data['curric_coi'] = curric_coi
    data['percent_in_range'] = percent_in_range

    return data


def flatten_concurrent_courses(data):
    courses = []

    for index, row in data.iterrows():
        # Retrieve the concurrent_courses data for the row
        concurrent_courses = row.get('concurrent_courses')

        # Check if concurrent_courses is empty or None
        if not concurrent_courses:
            courses.append(None)
        else:
            # Create a set of the keys with spaces removed
            fixed_set = {key.replace(' ', '') for key in concurrent_courses.keys()}
            courses.append(fixed_set)

    # Update the DataFrame with the new concurrent_courses data
    data['concurrent_courses'] = courses
    return data


def remove_extra_columns(data):
    del data['coi_data']
    del data['gpa_distro']
    del data['prereq_graph']
    del data['prereq_string']
    return data


def flatten_prereq(data):
    # Lists to hold the information for each course
    has_prereq_of = []
    is_prereq_for = []

    # Iterate over the DataFrame rows
    for index, row in data.iterrows():
        # Initialize default values for when 'prereq_graph' is None or doesn't contain the required keys
        has_set = {None}
        is_set = {None}

        # Check if 'prereq_graph' is not None and contains the necessary structure
        prereq_graph = row.get('prereq_graph')
        if prereq_graph:
            has_edges = prereq_graph.get('x', {}).get('edges', {}).get('from')
            is_edges = prereq_graph.get('x', {}).get('edges', {}).get('to')
            self_course_id = row.get('course_id')

            if has_edges:
                has_set = {course.replace(' ', '') for course in has_edges.values() if course != self_course_id}
            if is_edges:
                is_set = {course.replace(' ', '') for course in is_edges.values() if course != self_course_id}

        # Add the processed sets to the corresponding lists
        has_prereq_of.append(has_set if has_set else {None})
        is_prereq_for.append(is_set if is_set else {None})

    # Add the new lists as columns to the DataFrame
    data['has_prereq'] = has_prereq_of
    data['is_prereq'] = is_prereq_for
    return data


def flatten_course_offered(data):
    offered = []
    quarter_mapping = {
        'A': 'autumn',
        'W': 'winter',
        'Sp': 'spring',
        'S': 'summer'
    }
    for index in data.index:
        quarter_set = set()
        # print(data.loc[index]['course_offered'])
        if data.loc[index]['course_offered'] != None:
            line = data.loc[index]['course_offered']
            if 'jointly' in line:
                if ';' in line:
                    line = line.split(';')[1].strip()
                else:
                    line = ''
            if ',' in line:
                line = line.split(',')[0].strip()
            for abbrev in quarter_mapping:
                if abbrev in line:
                    quarter_set.add(quarter_mapping[abbrev])

            if line == '':
                quarter_set.add(None)
        else:
            quarter_set.add(None)
        offered.append(quarter_set)
    data['course_offered'] = offered
    return data


def flatten_description(data):
    prepositions = {'aboard', 'about', 'above', 'across', 'after', 'against', 'along', 'among', 'around', 'before',
                    'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'concerning', 'considering', 'despite',
                    'during', 'except', 'inside', 'outside', 'regarding', 'round', 'since', 'through', 'toward',
                    'under', 'underneath', 'until', 'within', 'without'}

    for index in data.index:
        string_set = set()
        course_description = data.loc[index, 'course_description']  # Use loc to access the cell directly

        if course_description:
            # Remove punctuation and split into words
            string = course_description.replace(',', '').replace('.', '').replace(';', '').replace(':', '').replace('/',
                                                                                                                    ' ')
            string = string.replace(')', '').replace('(', '').split()
            # Create a set of words that are not prepositions
            string_set = {word for word in string if
                          word.lower() not in prepositions and len(word) > 4 and not word.isdigit()}
        # Update the 'course_description' for each row in the DataFrame
        if string_set == set():
            data.at[index, 'course_description'] = set({None})
        else:
            data.at[index, 'course_description'] = string_set  # Convert set back to string

    return data


def get_department_dict():
    with open('files/department_html_dict.pkl', 'rb') as handle:
        html_dict = pickle.load(handle)
    dep_word_list = {}
    for department in html_dict:
        soup = BeautifulSoup(str(html_dict[department]), 'html.parser')
        dep_string = soup.h1.text.split('\n')
        dep_words = [string for string in dep_string if string != 'UW TACOMA']
        dep_words = [string for string in dep_words if string != 'UW BOTHELL']
        dep_words = [string for string in dep_words if string]
        dep_word_list[department] = dep_words
    return dep_word_list


def add_departments(data):
    dep_dict = get_department_dict()
    dep_list = []
    for index in data.index:
        key = str(data.loc[index, 'department_abbrev']).replace(' ', '')
        if key in dep_dict:
            dep_list.append(set(dep_dict[key]))
        else:
            dep_list.append({None})
    data['departments'] = dep_list
    return data


data = average(data)
print(data)
print(data.loc['TMATH208'])

data = average_no_zero(data)
print(data)
print(data.loc['TMATH208'])
data = percent_mastered(data)
print(data)
print(data.loc['TMATH208'])
data = flatten_coi_data(data)
print(data)
print(data.loc['TMATH208'])
data = flatten_concurrent_courses(data)
print(data)
print(data.loc['TMATH208'])
data = flatten_prereq(data)
print(data)
print(data.loc['TMATH208'])
data = add_level(data)
print(data)
print(data.loc['TMATH208'])
data = remove_extra_columns(data)
print(data)
print(data.loc['TMATH208'])
data = flatten_course_offered(data)
print(data)
print(data.loc['TMATH208'])
data = flatten_description(data)
print(data)
print(data.loc['TMATH208'])
data = add_departments(data)
print(data)
print(data.loc['TMATH208'])
data.to_pickle('./files/temp_data_frame.pkl')
# for index in data.index:
#     print(data.loc[index, 'departments'])
print(data)
