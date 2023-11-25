import re

out = open('urlfooter.txt', 'w')
with open('courses.txt') as file:
    file.__next__()
    for line in file:
        x = re.search('[A-Z\s]*(?=\d)', line)
        y = re.search('0*\d+', line)
        if int(y.group()) < 500:
            out.write(str(x.group() + y.group()).replace(' ', '') + ', ' + x.group() + y.group() + '\n')

out.close()
read = open('urlfooter.txt', 'r')
print(read.read())

#
#
# import requests
# from bs4 import BeautifulSoup
# import re
#
# with open('./coursesmain/Seattle.htm') as file:
#     soup = BeautifulSoup(file.read(), 'html.parser')
#     # print(soup)
#     for line in soup.findAll('li'):
#         print(re.search(re.search('(\b\w+\b,)+\.html')))
#
#     print(row)
#     # for r in row:
#     #     string = r.p.b.text
#     #     print(string)
#     #     f.write(string)
#     #     f.write('\n')
