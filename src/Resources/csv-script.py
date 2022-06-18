import os
from io import StringIO

mergedFileName = 'time_data.csv'
mergedData = StringIO()
rootDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logsDir = os.path.join(rootDir, 'Resources', 'time')
headers = 'declare time, millis\trun time, millis\tfact name\tfact params\tcurator type\n'
mergedData.write(headers)

files = os.listdir(logsDir)
for file in files:
    if mergedFileName != file:
        with open(os.path.join(logsDir, file), 'r') as fd:
            data = fd.read().replace(headers, "")
            mergedData.write(data)
    pass

fileName = os.path.join(logsDir, mergedFileName)
with open(fileName, 'w') as fd:
    fd.write(mergedData.getvalue())

mergedData.close()
print('save time record file: ' + fileName)