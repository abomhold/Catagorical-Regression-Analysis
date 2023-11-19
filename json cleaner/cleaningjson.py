import json
from array import array

import pandas
from sklearn import preprocessing
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# dump = json.loads(open('dump.json', 'r').read())
# new = {}
# for course in dump:
#     if 'error' not in dump[course]:
#         new[course] = dump[course]
# cleandump.write(json.dumps(removeerrors()))
# cleandump.close()
# cleandump = open('cleandump.json','r')
# print(cleandump.read())

dump = open('cleandump.json', 'w')


# Remove errors




# Get to overall gpa
# totalcount = 0
# totalgpa = 0
# for course in dump:
#     for entry in dump[course]['gpa_distro']:
#         totalcount += entry['count']
#         totalgpa += entry['count'] * int(entry['gpa'])
#
# overallgpa = totalgpa / totalcount
#
#
# # Turn the gpa in to something useful
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
# def offsetfromoverall(course):
#     gpa = average(dump[course]['gpa_distro'])
#     return overallgpa - gpa
# for course in dump:
#     print(course)
#     print(offsetfromoverall(course))

# print(average(dump['TCSS305']['gpa_distro']))


# df = pd.DataFrame(dump)
# print(df)


# df.sort_index(key=lambda x1: int(x1).)
# df.index = df.index.astype(int)
# # df = df.reindex(sorted(df.columns[1:], key=lambda x: int(x.split('_')[-1][1:])), axis=1)
#
# df = df.sort_index(ascending=True)
# df = df.T
# y = df.columns.to_numpy().reshape(-1,1)
# x = df.T.values
# print(y)
# print(x)
# # x = df.iloc[:, 0].values
# # print(x)
# import json
#
#
#
# #gpa_dict = eval(open('datacollapsed.json', 'r').read())
# courses = eval(open('grades.dict', 'r').read())
# percents = {}
#
# for prefix in courses:
#     for number in courses[prefix]:
#         if average(prefix, number) != 0:
#             percents[prefix + number] = average(prefix, number)
#
# with open('percents', 'w') as file:
#     file.write(json.dumps(percents, sort_keys=True, indent=4))
#
# with open('percents', 'r') as file:
#     print(file.read())
# # json.dumps(data, sort_keys=True, indent=4)
