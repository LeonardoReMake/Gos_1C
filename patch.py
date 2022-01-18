import sys
import numpy as np

def patch(file1):
	result = ""
	instructions = []
	i = 0
	for line in file1:
		if ("#" not in line):
			result += line
			continue

		print(line)
		result = result[:-1]
		s1 = line.find('#', 1)
		s2 = line.find('#', s1+1)
		s3 = line.find('#', s2+1)
		start = int(line[1:s1])
		end = int(line[s1+1:s2])
		length = int(line[s2+1:s3])
		sequence = line[s3+1:]
		instructions.append((start, end, length, sequence, len(line)))
		print(start, end, length, sequence)

	print(result)
	offset = 0
	for inst in instructions:
		start = inst[0]
		end = inst[1]
		length = inst[2]
		sequence = inst[3]
		line_len = inst[4]

		# print(start, end, length, line_len)

		if (length == 0):
			# offset += line_len + 1
			result = result[:start] + result[end:]
			continue

		if (length != 0):
			# offset += line_len + 1
			result = result[:start] + sequence[:-1] + result[end:]

	return result


def open_file(file_name):
	try:
		file_dsc = open(file_name, 'r')
		return file_dsc
	except IOError:
		print("Error while opening %s. Check file name", file_name1)
		return None

def main(filename):
	file1 = open_file(filename)
	if file1 is None: return

	print(patch(file1))


if __name__ == "__main__":
	main(sys.argv[1])
