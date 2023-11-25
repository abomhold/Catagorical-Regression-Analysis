import json
import pandas as pd
import re

TOTAL_COUNTS = 2370259
OVERALL_GPA = 33.675253210725074

data = pd.read_pickle('files/trimmed_data_frame.pkl')
print(data)


def average(data):
    avg_list = []
    for course in data.index:
        totalcount = 0
        totalgpa = 0
        for grade in data.loc[course]['gpa_distro']:
            totalcount += grade['count']
            totalgpa += grade['count'] * int(grade['gpa'])
        avg_list.append(totalgpa / totalcount)
    data['gpa_avg'] = avg_list
    return data


def average_no_zero(data):
    temp = data
    avg_list = []
    for index in data.index:
        totalcount = 0
        totalgpa = 0
        for grade in data.loc[index]['gpa_distro']:
            if grade['gpa'] != '0':
                totalcount += grade['count']
                totalgpa += grade['count'] * int(grade['gpa'])
        avg_list.append(totalgpa / totalcount)
    data['gpa_avg_no_drops'] = avg_list
    return data


def percent_mastered(data):
    avg_list = []
    for index in data.index:
        total_count = 0
        mastered_count = 0
        for grade in data.loc[index]['gpa_distro']:
            total_count += grade['count']
            if int(grade['gpa']) >= 30:
                mastered_count += grade['count']
            # if total_count == 0:
            #     # print(data[index])
            #     avg_list.append(0)
        else:
            avg_list.append(mastered_count / total_count)
    data['percent_mastered'] = avg_list
    return data


def flatten_coi_data(data):
    course_coi = []
    course_level_coi = []
    curric_coi = []
    percent_in_range = []
    for index in data.index:
        course_coi.append(data.loc[index]['coi_data']['course_coi'])
        course_level_coi.append(data.loc[index]['coi_data']['course_level_coi'])
        curric_coi.append(data.loc[index]['coi_data']['curric_coi'])
        percent_in_range.append(data.loc[index]['coi_data']['percent_in_range'])
    data['course_coi'] = course_coi
    data['course_level_coi'] = course_level_coi
    data['curric_coi'] = curric_coi
    data['percent_in_range'] = percent_in_range
    return data


def flatten_concurrent_courses(data):
    courses = []
    for index in data.index:
        if data.loc[index]['concurrent_courses'] == {} or data.loc[index]['concurrent_courses'] == None:
            courses.append(None)
        else:
            courses.append(set(data.loc[index]['concurrent_courses'].keys()))
            # print(list(data.loc[index]['concurrent_courses'].keys()))
    data['concurrent_courses'] = courses
    return data


def remove_extra_columns(data):
    del data['coi_data']
    del data['gpa_distro']
    del data['prereq_graph']
    del data['prereq_string']
    return data


def flatten_prereq(data):
    has_prereq_of = []
    is_prereq_for = []
    for index in data.index:
        if data.loc[index]['prereq_graph'] != None:
            has_prereq_of.append(set(data.loc[index]['prereq_graph']['x']['edges']['from'].values()))
            is_prereq_for.append(set(data.loc[index]['prereq_graph']['x']['edges']['to'].values()))
        else:
            has_prereq_of.append(None)
            is_prereq_for.append(None)
    data['has_prereq_of'] = has_prereq_of
    data['is_prereq_for'] = is_prereq_for
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
    data['usually_offered'] = offered
    return data


data = average(data)
data = average_no_zero(data)
data = percent_mastered(data)
data = flatten_coi_data(data)
data = flatten_concurrent_courses(data)
data = flatten_prereq(data)
data = remove_extra_columns(data)
data = flatten_course_offered(data)
# data = data.T
# print(data.loc[data['course'] == 'TCSS305'])
# print(data[6374]['coi_data'])
# for index in data.index:
#     print(data.loc[index]['usually_offered'])
# if data.loc[index]['prereq_graph'] != None:
#         # temp = eval(str(data.loc[index]['prereq_graph']['x']['edges']['to']))
#         # print(
#         #     list(sorted({ele for val in data.loc[index]['prereq_graph']['x']['edges']['to'].values() for ele in val})))
#         # print(data.loc[index]['course'])
#         print(data.loc[index]['prereq_graph']['x']['nodes']['writing_crs'])
#         # print(set(data.loc[index]['prereq_graph']['x']['edges']['from'].values()))
# .loc[6380]
print(data.loc[6380])

# import json
# from array import array
#
# import pandas
# from sklearn import preprocessing
# from sklearn.datasets import make_classification
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split
# from sklearn.pipeline import make_pipeline
# from sklearn.preprocessing import StandardScaler
# import pandas as data
#
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split

#
# def offsetfromoverall(distro):
#     overallgpa = 32.37313217414929
#     overallcount = 235568
#     gpa = average(distro)
#     if gpa != 0:
#         return overallgpa - gpa
#     else:
#         return 0
#
#
# # Turn the gpa in to something useful
# def gettotal(distro):
#     totalcount = 0
#     for entry in distro:
#         totalcount += entry['count']
#     return totalcount
#
#
# def average(distro):
#     totalcount = 0
#     totalgpa = 0
#     for entry in distro:
#         totalcount += entry['count']
#         totalgpa += entry['count'] * int(entry['gpa'])
#     if totalcount == 0:
#         return 0
#     else:
#         return totalgpa / totalcount
#
#
# def averagewithoutzero(distro):
#     totalcount = 0
#     totalgpa = 0
#     for entry in distro:
#         if entry['gpa'] != '0':
#             totalcount += entry['count']
#             totalgpa += entry['count'] * int(entry['gpa'])
#     if totalcount == 0:
#         return 0
#     else:
#         return totalgpa / totalcount
# totaldistro = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0, '11': 0, '12': 0, '13': 0, '14': 0, '15': 0, '16': 0, '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, '22': 0, '23': 0, '24': 0, '25': 0, '26': 0, '27': 0, '28': 0, '29': 0, '30': 0, '31': 0, '32': 0, '33': 0, '34': 0, '35': 0, '36': 0, '37': 0, '38': 0, '39': 0, '40': 0}
#
# def gettotaldistro(distro):
#     for entry in distro:
#          #print(entry['gpa'])
#         #print(entry['count'])
#         totaldistro[entry['gpa']] += entry['count']
#
#
#
# def changevalues(course):
#     gettotaldistro(dump[course]['gpa_distro'])
#     dump[course]['gpaaverage'] = average(dump[course]['gpa_distro'])
#     dump[course]['gpaoffset'] = offsetfromoverall(dump[course]['gpa_distro'])
#     dump[course]['gpacount'] = gettotal(dump[course]['gpa_distro'])
#     dump[course]['dropcount'] = dump[course]['gpa_distro'][0]['count']
#     dump[course]['gpanodrop'] = averagewithoutzero(dump[course]['gpa_distro'])
#     # del dump[course]['gpa_distro']
#     dump[course]['gpaoffsetnodrop'] = overallgpa - dump[course]['gpanodrop']
#     gettotal(dump[course]['gpa_distro'])
#
# # split courses with gpa
# def splitcourses():
#     def removenogpa(course):
#         gpa = average(dump[course]['gpa_distro'])
#         if gpa == 0:
#             nogpacourses[course] = dump[course]
#         else:
#             gpacourses[course] = dump[course]
#
#     nogpacourses = {}
#     gpacourses = {}
#     for course in dump:
#         removenogpa(course)
#
#     with open('nogpadump.json', 'w') as file:
#         file.write(json.dumps(nogpacourses, sort_keys=True, indent=4))
#
#     # print(open('nogpadump.json', 'r').read())
#
#     with open('gpadump.json', 'w') as file:
#         file.write(json.dumps(gpacourses, sort_keys=True, indent=4))
#     # print(open('gpadump.json', 'r').read())
#
#
# # splitcourses()
# dump = json.loads(open('gpadump.json', 'r').read())
# temp.json = dump
#
# for course in temp.json:
#     changevalues(course)
#
# print(totaldistro)
#
# #
# # with open('working.json', 'w') as file:
# #     file.write(json.dumps(dump, sort_keys=True, indent=4))
#
# # Remove options
#
#
# # print(dump)
#
# # temp.json = json.dumps(dump, sort_keys=True, indent=4)
# # with open('working.json', 'w') as file:
# #     file.write(temp.json)
#
# # for course in temp.json:
# #     print(dump[course]['gpaoffset'])
#
# # print(offsetfromoverall('TCSS305'))
# #
# df = data.DataFrame(dump).T
# df = df[['gpaoffsetnodrop','gpaaverage', 'gpaoffset', 'gpacount','dropcount','gpanodrop']]
# df = df.sort_values(by='gpaoffsetnodrop', ascending=True)
#
# # print(df.to_string())
# #print(json.dumps(dump['TCSS305'], sort_keys=True, indent=4))
#
# # df.sort_index(key=lambda x1: int(x1).)
# # df.index = df.index.astype(int)
# # # df = df.reindex(sorted(df.columns[1:], key=lambda x: int(x.split('_')[-1][1:])), axis=1)
# #
# # df = df.sort_index(ascending=True)
# # df = df.T
# # y = df.columns.to_numpy().reshape(-1,1)
# # x = df.T.values
# # print(y)
# # print(x)
# # # x = df.iloc[:, 0].values
# # # print(x)
# # import json
# #
# #
# #
# # #gpa_dict = eval(open('datacollapsed.json', 'r').read())
# # courses = eval(open('grades.dict', 'r').read())
# # percents = {}
# #
# # for prefix in courses:
# #     for number in courses[prefix]:
# #         if average(prefix, number) != 0:
# #             percents[prefix + number] = average(prefix, number)
# #
# # with open('percents', 'w') as file:
# #     file.write(json.dumps(percents, sort_keys=True, indent=4))
# #
# # with open('percents', 'r') as file:
# #     print(file.read())
# # # # json.dumps(data, sort_keys=True, indent=4)
# # def offsetfromoverall(course):
# #     gpa = average(dump[course]['gpa_distro'])
# #     if gpa != 0:
# #         return overallgpa - gpa
