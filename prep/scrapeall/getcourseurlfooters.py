import requests
from bs4 import BeautifulSoup
import re

campuses = {'Bothell.htm', 'Seattle.htm', 'Tacoma.htm'}


def get_url_footers(campuses):
    url_footers = []
    for campus in campuses:
        with open('./files/' + campus) as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
            for line in soup.findAll('li'):
                match = re.search('(?<=href=")[a-zA-Z.]+(?=">)', str(line.a))
                if match:
                    if campus == 'Bothell.htm':
                        url_footers += '/crscatb/' + match.group()
                    elif campus == 'Seattle.htm':
                        url_footers += '/crscat/' + match.group()
                    elif campus == 'Tacoma.htm':
                        url_footers += '/crscatt/' + match.group()


def get_course_html():
    with open('output/courseurlfooter.txt', 'r') as file:
        html_dict = {}
        for line in file:
            url = 'https://www.washington.edu/students' + line[:-1]
            department_abbrev = line.split('/')[2].split('.')[0].upper()
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            print(soup)
            html_dict[department_abbrev] = soup


get_url_footers(campuses)

with open('output/courseurlfooter.txt', 'r') as file:
    print(file.read())
