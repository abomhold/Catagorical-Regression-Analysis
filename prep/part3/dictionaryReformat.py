import json
from collections import defaultdict

gpa_dict = eval(open('../old/grades.dict', 'r').read())
gpaoverthreecollapsed = {}
gpaoverthreeexpanded = defaultdict(dict)

def average(prefix, number):
    gpa = gpa_dict[prefix][number]
    total, three = 0, 0
    for key in gpa.keys():
        total += gpa.get(key)
        if 40 >= int(key) >= 30:
            three += gpa.get(key)
    if total == 0:
        return 0
    else:
        three = three / total
        return three


for prefix in gpa_dict:
    for number in gpa_dict[prefix]:
        gpaoverthreecollapsed[str(prefix + number)] = average(prefix, number)
        gpaoverthreeexpanded[prefix][number] = average(prefix, number)


print(str(json.dumps(gpaoverthreecollapsed)))
print(str(json.dumps(gpaoverthreeexpanded)))
