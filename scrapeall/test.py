from bs4 import BeautifulSoup

with open('./output/coursesrawhtml', 'r') as file:
    soup = BeautifulSoup(file.read(), 'html.parser')
    soup = soup.findAll('a', {"name": lambda l: l})
    for line in soup:
        print(line.p.b.text)
