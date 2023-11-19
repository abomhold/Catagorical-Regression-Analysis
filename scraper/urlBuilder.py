urls = open('urlsforjsons.txt', 'w')
with open('urlfooter.txt') as file:
    for line in file:
        string = str(line.rstrip()).split(',')
        url = string[0] + ',' + 'https://dawgpath.uw.edu/api/v1/courses/details/' + string[1][1:] + '\n'
        urls.write(url)
        print(url)

urls.close()
