import pickle

import requests
from bs4 import BeautifulSoup

with open('output/courseurlfooter.txt', 'r') as file:
    html_dict = {}
    for line in file:
        url = 'https://www.washington.edu/students' + line[:-1]
        department_abbrev = line.split('/')[2].split('.')[0].upper()
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        print(soup)
        html_dict[department_abbrev] = soup


with open('.pkl', 'wb') as handle:
    pickle.dump(html_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('filename.pickle', 'rb') as handle:
    b = pickle.load(handle)


# with open('output/coursesraw.html', 'r') as file:
#     print(file.read())


# ./files/allcoursesorted.json
# with open('./files/allcoursesorted.json', 'w') as file:
#     file.write(json.dumps(eval(open('./files/allcourse.json', 'r').read()), sort_keys=True))
#
# with open('./files/allcoursesorted.json', 'r') as file:
#         print(file.read())
