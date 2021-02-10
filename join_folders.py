import sys, glob, os, shutil


bigfolder = sys.argv[1]

directories = os.listdir(bigfolder)


for dir in directories:
	files = os.listdir(bigfolder + dir)
	for fi in files:
		# print(bigfolder + dir + '/'+ fi, bigfolder + fi)
		shutil.move(bigfolder + dir + '/'+ fi, bigfolder + fi)

for dir in directories:
	os.rmdir(bigfolder + dir)




