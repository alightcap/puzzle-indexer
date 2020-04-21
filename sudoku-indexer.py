import sys
import PyPDF2
import re
from pprint import pprint
import os

# file_name = sys.argv[1]

# the goal here is to read each puzzle and put a tuple of (puzzle_type, point_value) into this list
# then write to a txt file that meta data.


def extract_data(file_name):
	points = []
	titles = []
	with open(file_name, 'rb') as f:
		pdf_reader = PyPDF2.PdfFileReader(f)

		for page in range(pdf_reader.numPages):
			page = pdf_reader.getPage(page).extractText()
			lines = page.split('\n')
			filtered_lines = list(map(lambda s: s.strip(), filter(lambda t: t.strip() != '', lines)))

			for line_num, line in enumerate(filtered_lines):
				# look for the word points
				# is there a digit in that line?
				#   if so, grab it
				# otherwise:
				#   look up to grab it
				# looks like the largest window is 5 lines up?

				if 'point' in line:
					if line[0].isdigit():
						points.append(int(line.split()[0]))
					else:
						points.append(int(filtered_lines[line_num-1]))
				
					# now keep looking up until you find the puzzle title?
					for i in range(5):
						if 'sudoku' in filtered_lines[line_num-i].lower():
							if 'sudoku' == filtered_lines[line_num-i].lower():
								titles.append(' '.join(filtered_lines[line_num-i-1:line_num-i+1]))
								break
							else:
								titles.append(filtered_lines[line_num-i])
								break


		meta_data = list(zip(titles, points))

		output_file = file_name.split('.')[0]+'_data.txt'
		with open(output_file, 'w') as f:
			for title, score in meta_data:
				f.write(f'{title}, {score}\n')

		return meta_data

folder = sys.argv[1]

all_files = os.listdir(folder)
sm_files = list(filter(lambda s: s.startswith('SM'), all_files))
print(sm_files)

for file in sm_files:
	extract_data(folder + '\\' + file)
# pprint(extract_data(file_name))
# extract_data(file_name)	
		# pprint(meta_data)
		# print(sum(points))