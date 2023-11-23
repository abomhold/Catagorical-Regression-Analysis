import json
import pandas as pd


with open('./files/all_raw.json', 'r') as file:
    data = eval(file.read())

newdump = eval(json.dumps(data))
# for entry in data:
#     #print(data[entry])
#     dump = eval(json.dumps(data[entry]))
#     print(dump)

for d in newdump:
    print(data[d].replace('\"', ''))


# with open('./files/temp', 'r') as file:
#     dump = json.loads(file.read())
#     print(dump)



# df = pd.DataFrame(data)
# print(df)

