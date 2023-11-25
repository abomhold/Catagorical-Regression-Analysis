import pickle

from bs4 import BeautifulSoup
import requests
import re

campuses = {'crscatb/', 'crscat/', 'crscatt/'}
UW_URL_HEADER = 'https://www.washington.edu/students/'


def get_urls(campus_list):
    urls = {}
    for campus in campus_list:
        url = UW_URL_HEADER + campus
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        for line in soup.findAll('li'):
            match = re.search('(?<=href=")[a-zA-Z.]+(?=">)', str(line.a))
            if match:
                department = match.group().split('.')[0].upper()
                urls[department] = url + match.group()
    return urls


def get_htmls(urls):
    html = {}
    for department in urls:
        print(urls[department])
        r = requests.get(urls[department])
        soup = BeautifulSoup(r.text, 'html.parser')
        print(soup)
        html[department] = soup
    return html


# html_dict = get_htmls(get_urls(campuses))
#
# with open('./files/department_html_dict.pkl', 'wb') as handle:
#     pickle.dump(html_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('files/department_html_dict.pkl', 'rb') as handle:
    b = pickle.load(handle)
    print(b)
    print(b.keys())
