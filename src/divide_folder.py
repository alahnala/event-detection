import sys, glob, os, shutil

bigfolder = sys.argv[1]
bigfolder = bigfolder + '/' if bigfolder[-1] != '/' else bigfolder
numThreads = int(sys.argv[2])

files = sorted(glob.glob(bigfolder + "*"))
numFiles = len(files)


for i in range(numThreads):
	os.makedirs(bigfolder + str(i), exist_ok=True)


counter = 0
for fi in files:
	new_dir = counter % numThreads
	newpath = '/'.join(fi.split('/')[:-1]) + '/' + str(new_dir) + '/' + fi.split('/')[-1]
	# print(newpath)
	shutil.move(fi, newpath)
	counter += 1




