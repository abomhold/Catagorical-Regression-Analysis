import json

import requests
import http.cookiejar as cookie
from bs4 import BeautifulSoup

cookies = "cookies.txt"
cookieJar = cookie.MozillaCookieJar('cookies.txt')
cookieJar.load()
Dict = {}
record = open('finaldump.json', 'w')
with open('urlsforjsons.txt') as file:
    for line in file:
        string = str(line).split(',')
        course = string[0]
        url = string[1]
        r = requests.get(url[:-1], cookies=cookieJar)
        Dict[course] = json.loads(r.text)
        print(Dict[course])
record.write(json.dumps(Dict))
record.close()
fr = open('finaldump.json', 'r')
print(fr.read())
fr.close()

# LOL might have just triggered something
