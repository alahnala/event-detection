import sys, glob, os, shutil


bigfolder = sys.argv[1]
outdir = sys.argv[2]

directories = os.listdir(bigfolder)


for dir in directories:
	files = os.listdir(bigfolder + dir)
	for fi in files:
		print(bigfolder + dir + '/'+ fi, bigfolder + outdir +  fi)
		# shutil.move(bigfolder + dir + '/'+ fi, bigfolder + outdir +  fi)

# for dir in directories:
# 	os.rmdir(bigfolder + dir)




