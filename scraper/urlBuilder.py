urls = open('urls.txt', 'w')
with open('coursecodes.txt') as file:
    for line in file:
        string = str(line.rstrip()).split(' ')
        url = string[0] + ',' + string[1] + ',' + 'https://dawgpath.uw.edu/api/v1/courses/details/' + string[0] + '%20' + string[1] + '\n'
        urls.write(url)
        print(url)

urls.close()
