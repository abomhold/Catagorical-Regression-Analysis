import json
import pickle
import sys
import requests
import http.cookiejar as cookie
from bs4 import BeautifulSoup
import re

HTML_URL_HEADER = 'https://www.washington.edu/students/'
JSON_URL_HEADER = 'https://dawgpath.uw.edu/api/v1/courses/'


# Function to retrieve course information from the UW API
def get_courses():
    # Define the campuses to fetch course data for
    campuses = {'seattle', 'tacoma', 'bothell'}
    courses = []

    # Loop through each campus
    for campus in campuses:
        # Construct the URL for the API call
        response = requests.get(f'{JSON_URL_HEADER}{campus}', cookies=cookie_jar)
        # Evaluate the text response to Python list
        courses += eval(response.text)
    return courses


# Function to build detailed course URLs from course data
def build_urls(courses):
    urls = {}

    # Loop through each course to construct its detailed URL
    for course in courses:
        key = course['key']
        url = f'{JSON_URL_HEADER}{key}'
        # Extract course prefix and number
        prefix, number = key[:-3].replace(' ', ''), key.split(' ')[-1]
        # Store the full URL with the course key
        urls[prefix + number] = url
    return urls


# Function to fetch course data in JSON format from URLs
def get_jsons(urls):
    raw_jsons = {}

    # Loop through each URL and fetch the JSON data
    for key, url in urls.items():
        response = requests.get(url, cookies=cookie_jar)
        # Parse the JSON response
        raw_jsons[key] = json.loads(response.text)
        # Log output to a file
        print(key, raw_jsons[key], file=log_file)
    return raw_jsons


# Function to scrape department information from UW course catalog pages
def build_department_urls():
    # Define the URL suffix for each campus
    campuses = {'crscatb/', 'crscat/', 'crscatt/'}
    urls = {}

    # Loop through each campus to construct department URLs
    for campus in campuses:
        url = HTML_URL_HEADER + campus
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Loop through each link header to find department URLs
        for line in soup.findAll('li'):
            match = re.search('(?<=href=")[a-zA-Z.]+(?=">)', str(line.a))
            if match:
                department = match.group().split('.')[0].upper()
                # Store the full URL for each department
                urls[department] = url + match.group()
    return urls


def scrape_and_save_html(urls):
    html_dict = {}

    # Loop through each department URL to scrape its HTML content
    for department, dep_url in urls.items():
        response = requests.get(dep_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Store the prettified HTML content
        html_dict[department] = soup.prettify()
    return html_dict


def process_department_html(html_dict):
    dep_word_list = {}

    # Process the HTML content to extract department words
    for department, html_content in html_dict.items():
        soup = BeautifulSoup(html_content, 'html.parser')
        # Extract and clean the department header text
        dep_string = soup.h1.text.replace('\n', '').replace('   ', '  ').split('  ')
        # Filter out unwanted words
        dep_words = [string for string in dep_string if string and string not in ('UW TACOMA', 'UW BOTHELL')]
        # Store the words for each department
        dep_word_list[department] = dep_words

    return dep_word_list


###################################################################
# COLLECT DEPARTMENT INFORMATION FROM ONLINE COURSE CATALOGUE

# # First build the department urls
# department_urls = build_department_urls()

# # Scrape the department course catalogue for department names
# html_content = scrape_and_save_html(department_urls)

# # To reduce server time scrape all html first
# # Save to file and then continue processing
# # Run once then comment out
# with open('./files/department_html_content.pkl', 'wb') as handle:
#     pickle.dump(html_content, handle, protocol=pickle.HIGHEST_PROTOCOL)

# For multiple runs just read from file
with open('./files/department_html_content.pkl', 'rb') as handle:
    html_dict = pickle.load(handle)

# Filter the department HTML to find the department keywords
processed_departments = process_department_html(html_dict)

# print(processed_departments)
with open('./files/departments.pkl', 'wb') as handle:
    pickle.dump(processed_departments, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('./files/departments.pkl', 'rb') as handle:
    html_dict = pickle.load(handle)
print(html_dict)

#################################################################
# COLLECT ALL COURSE JSONs
# TIME INTENSIVE

# Requires valid cookie file
# Instructions on how to generate your own in the '/files/cookie.txt'
# Set up cookie jar
cookie_jar = cookie.MozillaCookieJar("files/cookies.txt")
cookie_jar.load()

# Set up logging to a file
log_file = open('./files/log', 'w')
sys.stderr = log_file

# Get the courses from each campus's top level JSON
courses = get_courses()
# Build the urls for each course
urls = build_urls(courses)
# Collect the JSON for each course
courses_json = get_jsons(urls)

# Save the course JSON data
# with open('files/all_raw.json', 'w') as file:
#     json.dump(courses_json, file)

# Restore standard error and close log file
sys.stderr = sys.__stderr__
log_file.close()
##############################################################
