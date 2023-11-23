import json
import requests
import http.cookiejar as cookie
import re

cookie_jar = cookie.MozillaCookieJar("files/cookies.txt")
cookie_jar.load()


def getcourses():
    campuses = {'seattle', 'tacoma', 'bothell'}
    courses = []
    for campus in campuses:
        r = requests.get("https://dawgpath.uw.edu/api/v1/courses/" + campus, cookies=cookie_jar)
        courses += eval(r.text)
    return courses


def buildurls(courses):
    urls = {}
    for course in courses:
        string = course['key']
        url = 'https://dawgpath.uw.edu/api/v1/courses/details/' + string
        prefix = string[:-3].replace(' ', '')
        string = string.split(' ')
        number = string[len(string) - 1]
        urls[prefix + number] = url
    return urls


def getjsons(list):
    raw_jsons = {}
    for entry in list:
        r = requests.get(list[entry], cookies=cookie_jar)
        raw_jsons[entry] = r.text
        print(entry + '\n' + raw_jsons[entry])
    return raw_jsons



with open('./files/allurls', 'w') as file:
    file.write(json.dumps(buildurls(getcourses())))

with open('./files/allurls', 'r') as file:
    print(file.read())
    # file.write(json.dumps(getjsons(buildurls(getcourses())), sort_keys=True, indent=2))