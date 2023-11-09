def average(prefix, number):
    gpa = eval(open('grades.dict', 'r').read())[prefix][number]
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
    _one = str(round(_one / total * 100, 2)) + '%'
    one = str(round(one / total * 100, 2)) + '%'
    two = str(round(two / total * 100, 2)) + '%'
    three = str(round(three / total * 100, 2)) + '%'
    print('COURSE:  ' + prefix + ' ' + number + '\n' + 'TOTAL NUMBER OF STUDENTS:  ' +
          str(total) + '\n' + '0.0 - 0.9:  ' + _one + '\n' + '1.0 - 1.9:  ' + one + '\n' +
          '2.0 - 2.9:  ' + two + '\n' + '3.0 - 4.0:  ' + three + '\n')


course = ['TCSS', '440']

average(course[0], course[1])
