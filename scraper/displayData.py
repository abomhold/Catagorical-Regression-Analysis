fw = open('cleandata.txt', 'w')
with open('dataAll.txt') as file:
    for line in file:
        string = line.split(',')
        if string[2] != '{}\n' and string[2] != '{***ERROR***}\n':
            fw.write(','.join(string))

fw.close()
fr = open('cleandata.txt', 'r')
print(fr.read())
fr.close()