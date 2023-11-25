def average(prefix, number):
    gpa = courses[prefix][number]
    total, _one, one, two, three = 0, 0, 0, 0, 0
    for key in gpa.keys():
        total += gpa.get(key)
        if int(key) < 10:
            _one += gpa.get(key)
        if 20 > int(key) >= 10:
            one += gpa.get(key)
        if 30 > int(key) >= 20:
            two += gpa.get(key)
        if 40 >= int(key) >= 30:
            three += gpa.get(key)
    if total == 0:
        return 0
    else:
        _one = str(_one / total)
        one = str(one / total)
        two = str(two / total)
        three = str(three / total)
        out = str(prefix) + ',' + str(number) + ',' + str(total) + ',' + str(_one) + ',' + str(one) + ',' + str(
            two) + ',' + str(three) + '\n'
        print(out)
        return out


courses = eval(open('../old/grades.dict', 'r').read())
with open('files/GPA_Distro.csv', 'w') as file:
    file.write('PREFIX, NUMBER, TOTAL, 0.0-.9, 1.0-1.9, 2.0-2.9, 3.0-4.0\n')
    for prefix in courses:
        for number in courses[prefix]:
            if average(prefix, number) != 0:
                file.write(average(prefix, number))
