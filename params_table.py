import latex_table
import sys


'''
The ToPMine algorithm uses the minimum support of 40 to find all frequent
phrases and phrases were given a limit to search no more than 5-gram
FP-Growth algorithm used a minimum support of 8
θ = 3
dampening coefficient, ωt,
α = 10, β = .05, and χ = .5.
'''

#specified parameters
def print_specified(data):
	# headers = ["ToPMine minsupport", "ToPMine n-gram",  "FPgrowth minsupport", "$\\theta$", "$\omega$", "$\\alpha$", "$\\beta$", "$\chi$", "$\\tau$"]
	headers = ["ToPMine minsupport", "ToPMine n-gram",  "FPgrowth minsupport", "$\\theta$", "$\omega$", "$\\alpha$", "$\\beta$", "$\chi$", "$\\tau$"]
	default = ["40", "5", "8", "3", "0.1", "10", ".05", ".5", "24hr"]
	# experiment = ["15", "5", "1", "2", "0.1", "10", ".05", ".5", "24hr"]
	latex_table.print_latex_table(data=[default, data], header=headers, caption="Paper specified parameters",color="cyan")

def print_other(data):
	stopwords=["replication","topmine","nltk"]
	headers = ["ToPMine \#topics", "ToPMine $\\alpha$", "Stopwords"]
	latex_table.print_latex_table(data=[data], header=headers, caption="Parameters used that were not specified by the authors", color="blue")


def main():
	data = sys.argv[1:10]
	print_specified(data)
	data = sys.argv[10:]
	print_other(data)
	return

if __name__ == "__main__":
	main()
