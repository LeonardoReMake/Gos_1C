import sys
import numpy as np

# Matrix of editing distances
distances = None 

def get_str(seq):
	return ''.join([chr(num) for num in seq])

def make_instructions(path, seq1, seq2):
	result = []

	m_sequence = []
	m_start = 0
	m_end = 0
	is_modifying = False

	cur_point = path[0]
	prev_point = path[0]
	path.pop(0)

	# print("current (i, j): %d, %d", cur_point[0], cur_point[1])

	while (len(path) != 0):
		prev_point = cur_point
		cur_point = path[0]
		path.pop(0)

		# print("\n")
		# print("current (i, j): %d, %d", cur_point[0], cur_point[1])
		# print("prev (i, j): %d, %d", prev_point[0], prev_point[1])

		# print("m_start: %d", m_start)
		# print("m_end: %d", m_end)
		# print("is_modifying: %b", is_modifying)
		# print("m_sequence: %s", m_sequence)

		is_diagonal = (cur_point[0] == prev_point[0] - 1) and (cur_point[1] == prev_point[1] - 1)
		
		# If cur_point is in diagonal and the current characters are the same 
		if (is_diagonal and seq1[cur_point[0]] == seq2[cur_point[1]]):
			if (is_modifying):
				is_modifying = False
				instruction = "#" + str(m_start) + "#" + str(m_end) + "#" + str(len(m_sequence)) + "#" + get_str(m_sequence)
				result.append((m_start, instruction))
				m_sequence = []
			continue

		# If cur_point is in diagonal but current character are different
		if (is_diagonal and seq1[cur_point[0]] != seq2[cur_point[1]]):
			if (not is_modifying):
				is_modifying = True
				m_end = prev_point[1] + 1 # Где заканчиваем заменять (возможно не нужен +1)
			m_start = cur_point[1] + 1 # Откуда начинаем заменять (возможно не нужен +1)
			m_sequence.append(seq2[cur_point[1]])
			continue

		# Need to delete from seq1
		if (cur_point[1] == prev_point[1]):
			if (not is_modifying):
				is_modifying = True
				m_end = prev_point[0] + 1
			m_start = cur_point[0] + 1 # Откуда начинаем заменять (возможно не нужен +1)
			continue

		# Need to append from seq1
		if (cur_point[0] == prev_point[0]):
			if (not is_modifying):
				is_modifying = True
				m_start = cur_point[1] + 1 # Откуда начинаем заменять (возможно не нужен +1)
				m_end = m_start
			m_sequence.append(seq2[cur_point[1]])
			continue

	# print("\n")
	# print("current (i, j): %d, %d", cur_point[0], cur_point[1])
	# print("prev (i, j): %d, %d", cur_point[0], cur_point[1])

	# print("m_start: %d", m_start)
	# print("m_end: %d", m_end)
	# print("is_modifying: %b", is_modifying)
	# print("m_sequence: %s", m_sequence)

	if (is_modifying):
		is_modifying = False
		instruction = "#" + str(m_start) + "#" + str(m_end) + "#" + str(len(m_sequence)) + "#" + get_str(m_sequence)
		result.append((m_start, instruction))
		m_sequence = []

	return result


# Restores path 
def restore_path(seq1, seq2):
	path = []

	i = distances.shape[0] - 1
	j = distances.shape[1] - 1

	path.append((i, j))
	while (i > 0 or j > 0):
		if (i == 0):
			path.append((i, j-1))
			j -= 1
			continue

		if (j == 0):
			path.append((i-1, j))
			i -= 1
			continue

		diagonal = distances[i-1][j-1]
		if (seq1[i-1] != seq2[j-1]):
			diagonal += 1

		next_step = np.amin(np.array([ distances[i-1][j] + 1, distances[i][j-1] + 1, diagonal ]))

		if (next_step == diagonal):
			path.append((i-1, j-1))
			i -= 1
			j -= 1
		elif (next_step == distances[i-1][j] + 1):
			path.append((i-1, j))
			i -= 1
		elif (next_step == distances[i][j-1] + 1):
			path.append((i, j-1))
			j -= 1

	return path

# Creates distance matrix between seq1 and seq2. Result returns in distances. 
def create_dist_matrix(seq1, seq2):
	global distances

	# Adding zero element to make room for first characters
	seq1 = np.insert(seq1, 0, 0)
	seq2 = np.insert(seq2, 0, 0)

	len1 = len(seq1)
	len2 = len(seq2)

	distances = np.zeros([len1, len2], dtype=int)

	for i in range(len1):
		for j in range(len2):
			if (i == 0 and j == 0): 
				distances[i][j] = 0
			elif (i == 0):
				distances[i][j] = j
			elif (j == 0):
				distances[i][j] = i
			elif (seq1[i] == seq2[j]):
				distances[i][j] = distances[i-1][j-1]
			else:
				distances[i][j] = np.amin(np.array([ distances[i-1][j], distances[i][j-1], distances[i-1][j-1] ])) + 1



def open_read_file(file_name):
	try:
		file_dsc = open(file_name, 'rb')
		sequence = np.array(bytearray(file_dsc.read()))
		file_dsc.close()
		return sequence
	except IOError:
		print("Error while opening %s. Check file name", file_name1)
		return None

def create_merge_text(file1, instructions):
	file1 = np.insert(file1, 0, 0)
	result = ""
	i = 0
	addition = 0
	for character in file1:
		if (len(instructions) > 0):
			first = instructions[-1]

		if (first[0] == i - addition): 
			result += "\n" + first[1] + "\n"
			addition += 2 + len(first[1])
			i += addition
			instructions.pop()
			
		result += chr(character)
		# print("i", i)
		# print("addition", addition)
		# print(result)
		# print(chr(character))
		i += 1

	return result

def main(file_name1, file_name2, outfile_name):
	file1 = open_read_file(file_name1)
	if file1 is None: return
	
	file2 = open_read_file(file_name2)
	if file2 is None: return

	create_dist_matrix(file1, file2)
	# print(file1)
	# print(file2)
	# print(distances)
	path = restore_path(file1, file2)
	instr = make_instructions(path, file1, file2)
	print(create_merge_text(file1, instr))



if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], "sys.argv[3]")