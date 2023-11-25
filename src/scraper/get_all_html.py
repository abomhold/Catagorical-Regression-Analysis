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
        print(soup.h1.text.split('\n'))
        html[department] = soup
    return html


def get_department_dict(html_dict):
    dep_word_list = {}
    for department in html_dict:
        soup = BeautifulSoup(str(html_dict[department]), 'html.parser')
        dep_string = soup.h1.text.split('\n')
        dep_words = [string for string in dep_string if string != 'UW TACOMA']
        dep_words = [string for string in dep_words if string != 'UW BOTHELL']
        dep_words = [string for string in dep_words if string]
        dep_word_list[department] = dep_words
    return dep_word_list


html_dict = get_htmls(get_urls(campuses))
dep_word_list = get_department_dict(html_dict)

# with open('./files/department_word_set.pkl', 'wb') as handle:
#     pickle.dump(dep_word_list, handle, protocol=pickle.HIGHEST_PROTOCOL)
#
# with open('files/department_html_dict.pkl', 'rb') as handle:
#     b = pickle.load(handle)
#     print(b)
#     print(b.keys())
