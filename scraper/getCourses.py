import requests
from bs4 import BeautifulSoup

f = open('courses.txt', 'w')
f.write('PREFIX, NUMBER, TITLE \n')
with open('../old/departments.txt') as file:
    for url in file:
        r = requests.get(url[:-1])
        soup = BeautifulSoup(r.text, 'html.parser')
        row = soup.findAll("a", {"name": lambda l: l and l.startswith('t')})
        for r in row:
            string = r.p.b.text
            print(string)
            f.write(string)
            f.write('\n')
