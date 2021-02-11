from termcolor import colored

def print_latex_table(data, header=None, alignment=None, caption=None, label=None, color=None):
	# '''
	# prints a latex formatted table.

	# helpful: use \usepackage{booktabs} in latex

	# data = 2D array
	# header = optional. Must be same length as data entries.
	# alignment = optional. 
	# '''

	if color:
		print(colored(format_latex_table(data, header, alignment, caption, label), color=color))
	else:
		print(format_latex_table(data, header, alignment, caption, label))

def format_latex_table(data, header, alignment=None, caption=None, label=None):
# '''
# returns a string for the latex table. 

# helpful: use \usepackage{booktabs} in latex

# data = 2D array
# header = optional. Must be same length as data entries.
# alignment = optional. if using, need "c", "l", or "r" (or anything else latex will take) for entry length. Or ex p{3cm} (other options)
# caption = optional.
# label = optional.
# '''
	#Checking inputs
	entry_len = len(header)
	if not all([len(entry) == entry_len for entry in data]):
		print("Header:", header)
		print("Data:", data)
		print("Data entries are not all the same length")
		return "Data entries are not all the same length"	
	if header:
		if len(header) != entry_len:
			print("Header length does not match entry length")
			return "Header length does not match entry length"
	header = [str(item) for item in header]
	for i, entry in enumerate(data):
		for j, cell in enumerate(entry):
			data[i][j] = str(data[i][j])

	if not alignment:
		columns = ''.join(['c' for i in range(entry_len)])
	else:
		columns = alignment
	table_string = "\\begin{table*}[ht!]\n\centering\n\small\n  \\begin{tabular}{%s}" % (columns)
	# print(table_string)

	#Create table header
	if header:
		header_str = '\n    \\toprule\n    '
		for h in header:
			h = h.replace('/', '\slash ').replace('~', '$\sim$').replace("_", "\_")
			header_str += "\\textbf{%s}  &  " % (h)
		header_str = header_str[:-3] + "\\\\\n    \\midrule"
	else:
		header_str = '\n    \\toprule'
	table_string += header_str

	# Add entries
	for entry in data:
		entry_str = "\n    "
		for dp in entry:
			dp = dp.replace('/', '\slash ').replace('~', '$\sim$').replace("_", "\_")
			entry_str += "{}  &  ".format(dp)
		entry_str = entry_str[:-3] + '\\\\' #to remove the last ampersand, 
		table_string += entry_str

	table_string += "\n    \\bottomrule"
	table_string +=	"\n  \\end{tabular}"
	if caption:
		caption = caption.replace('/', '\slash ').replace('~', '$\sim$').replace("_", "\_")
		table_string += "\n\\caption{%s}" % (caption)
	if label:
		label = label.replace('/', '\slash ').replace('~', '$\sim$ ').replace("_", "\_")
		table_string += "\n\\label{tab:%s}" % (label)
	table_string += "\n\\end{table*}"
	
	return table_string



def test():
	print('Table 1:\n')

	headers = ["Decoder Model", "Bleu score", "Calc info?", "Brev.Penalty", "ratio", "hypothesis length", "reference length"]
	data = [["hello", 1.0, 2, 3, 4, 5, 6], ["world", 1, 2, 3, 4, 5, 6], ["this", 1, 2, 3, 4, 5, 6], ["table", 1, 2, 3, 4, 5, 6]]
	print_latex_table(data, header=headers, alignment=None, caption="Experiment", label="Experiment")

	print('\n\n\n')
	print('Table 2:\n')

	alignment = "p{12.0cm}llllll"
	print_latex_table(data, header=headers, alignment=alignment, caption="Experiment", label="Experiment")
	print('\n\n\n')
	print('Table 3:\n')
	alignment = ''.join(['r' if isinstance(dp, float) or isinstance(dp, int) else 'l' for dp in data[0]])
	print_latex_table(data, header=headers, alignment="p{12.0cm}llllll", caption="Experiment", label="Experiment")
	

if __name__ == "__main__":
	test()
