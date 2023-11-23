import json

with open('./files/allcoursesorted.json', 'w') as file:
    file.write(json.dumps(eval(open('./files/allcourse.json', 'r').read()), sort_keys=True))

with open('./files/allcoursesorted.json', 'r') as file:
        print(file.read())

# courses = json.load(open('./files/allcourse.json', 'r'))
# out = open('./files/allcourse.json', 'w')
# courses


# for course in courses:
#     string = course['key']
#     url = 'https://dawgpath.uw.edu/api/v1/courses/details/' + string + '\n'
#     print(url)

#     string = str(line.rstrip()).split(',')
#     url = string[0] + ',' + 'https://dawgpath.uw.edu/api/v1/courses/details/' + string[1][1:] + '\n'
#     urls.write(url)
#     print(url)
#
# urls.close()
# urls = open('urlsforjsons.txt', 'w')
