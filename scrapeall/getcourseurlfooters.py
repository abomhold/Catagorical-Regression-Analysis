from bs4 import BeautifulSoup
import re

campuses = {'Bothell.htm', 'Seattle.htm', 'Tacoma.htm'}


def getcoursefooters(campuses):
    with open('output/courseurlfooter.txt', 'w') as out:
        for campus in campuses:
            with open('./coursesmain/' + campus) as file:
                soup = BeautifulSoup(file.read(), 'html.parser')
                for line in soup.findAll('li'):
                    match = re.search('(?<=href=")[a-zA-Z.]+(?=">)', str(line.a))
                    if match:
                        if campus == 'Bothell.htm':
                            out.write('/crscatb/' + match.group() + '\n')
                        elif campus == 'Seattle.htm':
                            out.write('/crscat/' + match.group() + '\n')
                        elif campus == 'Tacoma.htm':
                            out.write('/crscatt/' + match.group() + '\n')



getcoursefooters(campuses)

with open('output/courseurlfooter.txt', 'r') as file:
    print(file.read())
