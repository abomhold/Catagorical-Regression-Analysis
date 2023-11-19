import json

def average(prefix, number):
    gpa = courses[prefix][number]
    total = 0
    for entry in gpa:
        total += gpa[entry]
    if total == 0:
        return 0
    else:
        out = {}
        for entry in gpa:
            out[entry] = gpa[entry] / total
        return out

#gpa_dict = eval(open('datacollapsed.json', 'r').read())
courses = eval(open('grades.dict', 'r').read())
percents = {}

for prefix in courses:
    for number in courses[prefix]:
        if average(prefix, number) != 0:
            percents[prefix + number] = average(prefix, number)

with open('percents', 'w') as file:
    file.write(json.dumps(percents, sort_keys=True, indent=4))

with open('percents', 'r') as file:
    print(file.read())
# json.dumps(data, sort_keys=True, indent=4)
