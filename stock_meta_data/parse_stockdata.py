import csv

import os

import json

data = []
for x in os.listdir("."):
	if x.startswith('company'):
		data += [i for i in csv.DictReader(open('{}'.format(x)))]


print len(data)
cleaned = []
for x in data[:]:
	flag = True
	for l in str(x['Symbol']).strip(" "):
		if str(l) not in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
			flag = False


	if flag:
		cleaned.append(x)
print len(cleaned)

with open('data.json','wb') as f:
	t = json.dumps(cleaned)
	print >> f, t