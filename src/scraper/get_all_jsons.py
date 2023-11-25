import json
import sys

import requests
import http.cookiejar as cookie
import logging

log_file = open('./files/log', 'w')
sys.stderr = log_file

cookie_jar = cookie.MozillaCookieJar("files/cookies.txt")
cookie_jar.load()


def get_courses():
    campuses = {'seattle', 'tacoma', 'bothell'}
    courses = []
    for campus in campuses:
        r = requests.get("https://dawgpath.uw.edu/api/v1/courses/" + campus, cookies=cookie_jar)
        courses += eval(r.text)
    return courses


def build_urls(courses):
    urls = {}
    for course in courses:
        string = course['key']
        url = 'https://dawgpath.uw.edu/api/v1/courses/details/' + string
        prefix = string[:-3].replace(' ', '')
        string = string.split(' ')
        number = string[len(string) - 1]
        urls[prefix + number] = url
    return urls


def get_jsons(urls):
    raw_jsons = {}
    for entry in urls:
        r = requests.get(urls[entry], cookies=cookie_jar)
        raw_jsons[entry] = json.loads(r.text)
        print(entry)
        print(raw_jsons[entry])
        sys.stdout = log_file
        print(entry)
        print(raw_jsons[entry])
        sys.stdout = sys.__stdout__
    return raw_jsons


with open('files/all_raw.json', 'w') as file:
    file.write(json.dumps(get_jsons(build_urls(get_courses()))))

sys.stderr = sys.__stderr__
log_file.close()




# print(get_courses())
# print(build_urls(get_courses()))
# print(get_jsons(build_urls(get_courses()))


# with open('./files/all_courses', 'r') as file:
#     print(file.read())
#
# with open('./files/allurls', 'r') as file:
#     print(file.read())

with open('files/all_raw.json', 'r') as file:
    print(file.read())
