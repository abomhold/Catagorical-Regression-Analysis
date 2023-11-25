import json
import pickle
import sys
import requests
import http.cookiejar as cookie
from bs4 import BeautifulSoup
import re

# Set up logging to a file and load cookies
log_file = open('./files/log', 'w')
sys.stderr = log_file
# cookie_jar = cookie.MozillaCookieJar("files/cookies.txt")
# cookie_jar.load()

UW_URL_HEADER = 'https://www.washington.edu/students/'


# Function to retrieve course information from the UW API
def get_courses():
    campuses = {'seattle', 'tacoma', 'bothell'}
    courses = []
    for campus in campuses:
        response = requests.get(f"https://dawgpath.uw.edu/api/v1/courses/{campus}", cookies=cookie_jar)
        courses += eval(response.text)
    return courses


# Function to build detailed course URLs from course data
def build_urls(courses):
    urls = {}
    for course in courses:
        key = course['key']
        url = f'https://dawgpath.uw.edu/api/v1/courses/details/{key}'
        prefix, number = key[:-3].replace(' ', ''), key.split(' ')[-1]
        urls[prefix + number] = url
    return urls


# Function to fetch course data in JSON format from URLs
def get_jsons(urls):
    raw_jsons = {}
    for key, url in urls.items():
        response = requests.get(url, cookies=cookie_jar)
        raw_jsons[key] = json.loads(response.text)
        print(key, raw_jsons[key], file=log_file)  # Log output
    return raw_jsons


# Function to scrape department information from UW course catalog pages
def build_department_urls():
    campuses = {'crscatb/', 'crscat/', 'crscatt/'}
    urls = {}
    for campus in campuses:
        url = UW_URL_HEADER + campus
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for line in soup.findAll('li'):
            match = re.search('(?<=href=")[a-zA-Z.]+(?=">)', str(line.a))
            if match:
                department = match.group().split('.')[0].upper()
                print('ADDING URL:' + url + match.group())
                urls[department] = url + match.group()
    return urls


def scrape_and_save_html(urls):
    html_dict = {}
    for department, dep_url in urls.items():
        response = requests.get(dep_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        print('ADDING HTML:' + soup.prettify())
        html_dict[department] = soup.prettify()
    return html_dict


def process_department_html(html_dict):
    dep_word_list = {}
    for department, html_content in html_dict.items():
        soup = BeautifulSoup(html_content, 'html.parser')
        dep_string = soup.h1.text.replace('\n', '').replace('   ', '  ').split('  ')
        dep_words = [string for string in dep_string if string and string not in ('UW TACOMA', 'UW BOTHELL')]
        print('FOR DEPARTMENT: ' + department)
        print('ADDING WORDS: ' + str(dep_words))
        dep_word_list[department] = dep_words

    return dep_word_list


# COLLECT DEPARTMENT INFORMATION FROM ONLINE COURSE CATALOGUE

# First build the department urls
department_urls = build_department_urls()
# Scrape the department course catalogue for department names
html_content = scrape_and_save_html(department_urls)
# To reduce server time scrape all html first
# Save to file and then continue processing
# Run once then comment out
with open('./files/department_html_content.pkl', 'wb') as handle:
    pickle.dump(html_content, handle, protocol=pickle.HIGHEST_PROTOCOL)
# For multiple runs just read from file
with open('./files/department_html_content.pkl', 'rb') as handle:
    html_dict = pickle.load(handle)
# Filter the department HTML to find the department keywords
processed_departments = process_department_html(html_dict)
print(processed_departments)

# COLLECT ALL COURSE JSONs

# Requires valid cookie file
# Instructions on how to generate your own in the '/files/cookie.txt'

# courses_json = get_jsons(build_urls(get_courses()))

# Save the course JSON data
# with open('files/all_raw.json', 'w') as file:
#     json.dump(courses_json, file)

# Restore standard error and close log file
sys.stderr = sys.__stderr__
log_file.close()
