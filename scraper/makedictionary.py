import json
from collections import defaultdict

fw = open('../datacollapsed.json', 'w')
data = defaultdict(dict)
with (open('cleandata.txt') as file):
    for line in file:
        string = line.split(',')
        course = string[0]
        number = string[1]
        gpa = ','.join(string[2:]).replace('\'', '\"')
        data[course+number] = json.loads(gpa)

fw.write(json.dumps(data, sort_keys=True, indent=4))
fw.close()
fr = open('../datacollapsed.json', 'r')
print(fr.read())
fr.close()
