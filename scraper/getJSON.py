import json

import requests
import http.cookiejar as cookie
from bs4 import BeautifulSoup

cookies = "cookies.txt"
cookieJar = cookie.MozillaCookieJar('cookies.txt')
cookieJar.load()
record = open('../old/dataAll.txt', 'w')
record.write('PREFIX, NUMBER, GPA \n')
with open('urls.txt') as file:
    for line in file:
        string = str(line).split(',')
        prefix = string[0]
        number = string[1]
        url = string[2].split(' ')[0]
        r = requests.get(url[:-1], cookies=cookieJar)
        gpa = json.loads(r.text).get('gpa_distro')
        Dict = {}
        try:
            for grade in gpa:
                Dict[str(grade.get('gpa'))] = grade.get('count')
        except TypeError:
            grade = prefix + ',' + number + ',' + '{***ERROR***}' + '\n'
        else:
            grade = prefix + ',' + number + ',' + str(Dict) + '\n'
        print(grade)
        record.write(grade)

record.close()
fr = open('../old/dataAll.txt', 'r')
print(fr.read())
fr.close()
