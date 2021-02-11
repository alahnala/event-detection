import sys

file = sys.argv[1]
counter = 0
with open(file) as f:
	items = f.readlines()
	for i in items:
		counter += int(i)
print(counter)