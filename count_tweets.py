import sys, glob
from tqdm import tqdm

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

tweetfiles = sys.argv[1]

total=0
tweetfiles = glob.glob(tweetfiles+"*")
for fname in tqdm(tweetfiles):
	with open(fname) as f:
		for i, l in enumerate(f):
			pass
		total += i + 1
print(total)
