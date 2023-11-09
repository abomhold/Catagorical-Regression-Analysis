import re
out = open('coursecodes.txt', 'w')
with open('courses.txt') as file:
    file.__next__()
    for line in file:
        x = re.search('[A-Z\s]*(?=\d)', line)
        y = re.search('0*\d+', line)
        out.write(x.group().replace(' ','') + ' ' + y.group() + '\n')

out.close()
read = open('coursecodes.txt', 'r')
print(read.read())