import pandas as pd


def averages(course):
    gpa = (course['gpa_distro'])
    prefix = str(course['course_id'][:-3]).replace(' ', '')
    number = course['course_id'][-3:]
    total, one, two, three, four = 0, 0, 0, 0, 0
    for entry in gpa:
        # print(entry.get('gpa'))
        total += (entry.get('count'))
        if int(entry.get('gpa')) < 10:
            one += entry.get('count')
        if 20 > int(entry.get('gpa')) >= 10:
            two += entry.get('count')
        if 30 > int(entry.get('gpa')) >= 20:
            three += entry.get('count')
        if 40 >= int(entry.get('gpa')) >= 30:
            four += entry.get('count')
    if total == 0:
        return 0
    else:
        one = str(one / total)
        two = str(two / total)
        three = str(three / total)
        four = str(four / total)
        out = str(prefix) + ',' + str(number) + ',' + str(total) + ',' + str(one) + ',' + str(two) + ',' + str(
            three) + ',' + str(four) + '\n'
        return out


data = pd.read_pickle('../complete/files/no_gpa_dataframe.pkl')

with open("files/gpa_history.csv", 'w') as file:
    file.write("PREFIX, NUMBER, SAMPLE SIZE, 0.0 - 0.9, 1.0 - 1.9, 2.0 - 2.9, 3.0 - 4.0 \n")
    for d in data:
        file.write(averages(data[d]))

with open("files/gpa_history.csv", 'r') as file:
    print(file.read())
