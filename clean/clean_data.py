import json
import pandas as pd
import re

# total_counts = 2370259
# overall_gpa = 33.675253210725074


with open('./files/all_raw.json', 'r') as file:
    data = file.read()

pd = pd.DataFrame(json.loads(data))


# print(pd.T.index)
# for course in pd:
#     print(course)


def remove_errors(pd):
    temp = pd
    for course in temp:
        if re.search('.*Course.*', str(pd[course]['error'])):
            del pd[course]


def remove_options(pd):
    temp = pd
    for course in temp:
        if pd[course]['prereq_graph'] != None:
            # (pd[course]['prereq_graph']['x']['options'])
            del pd[course]['prereq_graph']['x']['options']


def get_totals(pd):
    total_count = 0
    total_gpa = 0
    for course in pd:
        for entry in pd[course]['gpa_distro']:
            total_count += entry['count']
            total_gpa += entry['count'] * int(entry['gpa'])
    overall_gpa = total_gpa / total_count
    return {"total_count": total_count, "overall_gpa": overall_gpa}

print(pd.size)
remove_errors(pd)
remove_options(pd)
# coverted to constants
#get_totals(pd)
print(pd.size)





# for course in pd:
#     print(pd[course]['error'])

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
# import pandas as pd
#
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
#
# # Remove errors
# #
# # dump = json.loads(open('dump.json', 'r').read())
# # cleandump = open('cleandump.json', 'w')
# # new = {}
# # for course in dump:
# #     if 'error' not in dump[course]:
# #         new[course] = dump[course]
# # cleandump.write(json.dumps(new))
# # cleandump.close()
# # cleandump = open('cleandump.json', 'r')
# # print(cleandump.read())
#
# overallgpa = 32.37313217414929
# overallcount = 235568
# dump = json.loads(open('cleandump.json', 'r').read())
#
#

#
# removeoptions(dump)
#
#
# # print(dump)
#
# # Get to overall gpa
# # totalcount = 0
# # totalgpa = 0
# # for course in dump:
# #     for entry in dump[course]['gpa_distro']:
# #         totalcount += entry['count']
# #         totalgpa += entry['count'] * int(entry['gpa'])
# #
# # overallgpa = totalgpa / totalcount
# # print(totalgpa)
# # print(totalcount)
# # print(overallgpa)
# # 7626074
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
# temp = dump
#
# for course in temp:
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
# # temp = json.dumps(dump, sort_keys=True, indent=4)
# # with open('working.json', 'w') as file:
# #     file.write(temp)
#
# # for course in temp:
# #     print(dump[course]['gpaoffset'])
#
# # print(offsetfromoverall('TCSS305'))
# #
# df = pd.DataFrame(dump).T
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
