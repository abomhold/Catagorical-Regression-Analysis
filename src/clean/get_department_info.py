import pickle
from bs4 import BeautifulSoup
import requests
import re

with open('files/department_html_dict.pkl', 'rb') as handle:
    html_dict = pickle.load(handle)
dep_word_list = {}
for department in html_dict:
    # print(html_dict[department])
    soup = BeautifulSoup(str(html_dict[department]), 'html.parser')
    dep_string = soup.h1.text.split('\n')
    dep_words = [string for string in dep_string if string != 'UW TACOMA']
    dep_words = [string for string in dep_words if string != 'UW BOTHELL']
    dep_words = [string for string in dep_words if string]
    dep_word_list[department] = dep_words
    # print(dep_words)
    # print(dep_string)

with open('files/departement_dict.pkl', 'wb') as file:
    pickle.dump(dep_word_list, file)

with open('files/departement_dict.pkl', 'rb') as file:
    loaded_dict = pickle.load(file)
print(loaded_dict)