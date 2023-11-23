import requests
from bs4 import BeautifulSoup

with open('output/coursesrawhtml', 'w') as out:
    with open('output/courseurlfooter.txt', 'r') as file:
        for line in file:
            url = 'https://www.washington.edu/students' + line[:-1]
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            print(soup)
            out.write(str(soup))

with open('output/coursesrawhtml', 'r') as file:
    print(file.read())


# ./files/allcoursesorted.json
# with open('./files/allcoursesorted.json', 'w') as file:
#     file.write(json.dumps(eval(open('./files/allcourse.json', 'r').read()), sort_keys=True))
#
# with open('./files/allcoursesorted.json', 'r') as file:
#         print(file.read())
