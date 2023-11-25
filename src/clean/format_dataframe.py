import pandas as pd
import re

def remove_errors(data):
    temp = data
    for course in temp:
        if re.search('.*Course.*', str(data[course]['error'])):
            del data[course]
    return data

def remove_options(data):
    temp = data
    for course in temp:
        if data[course]['prereq_graph'] != None:
            del data[course]['prereq_graph']['x']['options']
    return data

def get_totals(data):
    total_count = 0
    total_gpa = 0
    for course in data:
        for entry in data[course]['gpa_distro']:
            total_count += entry['count']
            total_gpa += entry['count'] * int(entry['gpa'])
    overall_gpa = total_gpa / total_count
    return {"total_count": total_count, "overall_gpa": overall_gpa}


# remove none GPAs
def get_gpa_courses(data):
    temp = data
    for course in temp:
        print(course)
        # I have no clue why it is 9
        # I lost my labels somewhere....
        gpa = data[course][9]
        if gpa == []:
            del data[course]
    return data


# Remove gpa with 0 total counts
def get_gpa_courses_2(data):
    temp = data
    for course in temp:
        print(course)
        totalcount = 0
        for grade in temp[course][9]:
            totalcount += grade['count']
        if totalcount == 0:
            del data[course]
    return data
def remove_empty_collumn(data):
    data = data.T
    del data[14]
    return data

def add_headers(data):
    coloumns = ['coi_data', 'concurrent_courses', 'course_campus', 'course_credits', 'course_description', 'course_id',
            'course_offered', 'course_title', 'department_abbrev', 'gpa_distro', 'is_bottleneck', 'is_gateway',
            'prereq_graph', 'prereq_string']
    # data = pd.DataFrame(json.loads(data))
    data.columns = coloumns
    return data


# total_counts = 2370259
# overall_gpa = 33.675253210725074



data = pd.read_pickle('files/trimmed_data_frame.pkl')
#print(data.index)
#data.insert(0, "course",data.index, True)
data = data.reset_index(drop=True)
print(data)
data.to_pickle('./files/trimmed_data_frame.pkl')
#
#
# with open('./files/temp', 'w') as file:
#     data.to_json(file)
# print(data.T)
# data = remove_empty_collumn(data)
# data = get_gpa_courses(data)
# print(data)
# data = get_gpa_courses_2(data)
# print(data)
# data = remove_empty_collumn(data)
# print(data)
# data = add_headers(data)
# print(data)




# Write to file removed a lot of courses but
# not alot of space, the courses with gpa must
# be the heaviest

    # store = pd.HDFStore('store.h5')
    # store['data'] = data  # save it
    # store['data']  # load it




# wrote to temp.json file to reduce runtime SAVES 6MB
# remove_errors(data)
# remove_options(data)
# with open('./files/temp.json', 'w') as file:
#     data.to_json(file, orient='records')
# coverted to constants
# get_totals(data)

# Convert the gpa to something useful
# wrote to temp.json file to reduce runtime SAVES 6MB
# remove_errors(data)
# remove_options(data)
# with open('./files/temp.json', 'w') as file:
#     data.to_json(file, orient='records')
# coverted to constants
# get_totals(data)

# Convert the gpa to something useful

# remove none GPAs

# data = remove_empty_collumn(data)
# print(data)
# data = get_gpa_courses(data)
# data = get_gpa_courses_2(data)
# for course in data:
#     print(data[course][9])
# get_gpa_course_2(data)
# for course in data:
#     print(data[course][9])
