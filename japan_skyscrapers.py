from random import randint
from time import time
import os

clear = lambda: os.system('clear')

def check_dublicate_numbers(matrix):
	for row in matrix:
		for i, val in enumerate(row):
			for j, subval in enumerate(row):
				if val == subval and i != j:
					return False
	
	for curr_index in range(len(matrix[0])):
		for i, row in enumerate(matrix):
			for j, subrow in enumerate(matrix):
				if row[curr_index] == subrow[curr_index] and i != j:
					return False
	return True
	
def check_visability_accordance_for_row(row, visible_skyscrapers):
	current_visible = 0
	max_floors = row[0]
	for skyscraper in row:
		if skyscraper >= max_floors:
			current_visible += 1
			max_floors = skyscraper
	if current_visible == visible_skyscrapers:
		return True
	return False
	
def check_visability_accordance(matrix, visability_map):
	for i, visible_skyscrapers in enumerate(visability_map['top']):
		# generate skyscrapers row
		skyscrapers_row = [ x[i] for x in matrix ] #take every [i] skyscraper from matrix and generate list of them
		if not check_visability_accordance_for_row(skyscrapers_row, visible_skyscrapers):
			return False

	for i, visible_skyscrapers in enumerate(visability_map['bottom']):
		skyscrapers_row = [ x[i] for x in matrix ]
		skyscrapers_row.reverse()
		if not check_visability_accordance_for_row(skyscrapers_row, visible_skyscrapers):
			return False

	for i, visible_skyscrapers in enumerate(visability_map['left']):
		skyscrapers_row = matrix[i]
		if not check_visability_accordance_for_row(skyscrapers_row, visible_skyscrapers):
			return False

	for i, visible_skyscrapers in enumerate(visability_map['right']):
		skyscrapers_row = matrix[i]
		skyscrapers_row.reverse()
		if not check_visability_accordance_for_row(skyscrapers_row, visible_skyscrapers):
			return False
	return True

def complement_matrix(_matrix, needle_count=None, seed=None):
	matrix = [ [ col for col in row ] for row in _matrix ]
	side_size = len(matrix)
	if seed:
		#translate seed into side_size numeric system with +1 offset
		matrix_expanded = []
		needle_count = needle_count if needle_count else side_size**2 
		remains = seed
		while remains > 0 and len(matrix_expanded) < needle_count:
			remains, number = divmod(remains, side_size)
			# разобрать пограничный случай в старшем разряде
			matrix_expanded.append(number + 1)

		for i, row in enumerate(matrix):
			for j, col in enumerate(row):
				if not col:
					matrix[i][j] = matrix_expanded.pop() if len(matrix_expanded) > 0 else 1
	else:
		for i, row in enumerate(matrix):
			for j, col in enumerate(row):
				if not col:
					matrix[i][j] = randint(1, side_size)

	return matrix

def generate_matrix(side_size, visability_map=None):
	matrix = [ [ None for z in range(side_size) ] for y in range(side_size) ]
	needle_count = 0

	# OPTIMIZATION
	if visability_map:
		for i, visible_skyscrapers in enumerate(visability_map['top']):
			if visible_skyscrapers == 1:
				matrix[0][i] = side_size
			elif visible_skyscrapers == side_size:
				for j in range(side_size):
					matrix[j][i] = j+1

		for i, visible_skyscrapers in enumerate(visability_map['bottom']):
			if visible_skyscrapers == 1:
				matrix[side_size-1][i] = side_size
			elif visible_skyscrapers == side_size:
				for j in range(side_size):
					matrix[j][i] = side_size - j

		for i, visible_skyscrapers in enumerate(visability_map['left']):
			if visible_skyscrapers == 1:
				matrix[i][0] = side_size
			elif visible_skyscrapers == side_size:
				for j in range(side_size):
					matrix[i][j] = j+1

		for i, visible_skyscrapers in enumerate(visability_map['right']):
			if visible_skyscrapers == 1:
				matrix[i][-1] = side_size
			elif visible_skyscrapers == side_size:
				for j in range(side_size):
					matrix[i][j] = side_size - j

	for i, row in enumerate(matrix):
		for j, col in enumerate(row):
			if not col:
				needle_count += 1

	return (needle_count, matrix)

			
					
if __name__ == '__main__':
	side_size = int(input("ENTER SIDE SIZE: "))
	visability_map = {
		'top': [ int(x) for x in input('ENTER TOP: ') ],
		'bottom': [ int(x) for x in input('ENTER BOTTOM: ') ],
		'left': [ int(x) for x in input('ENTER LEFT: ') ],
		'right': [ int(x) for x in input('ENTER RIGHT: ') ],
	}
	use_random = input('ENTER "y" FOR RANDOM METHOD ELSE NOTHING: ')
	is_viewing = input('ENTER "y" FOR WATCHING MATRIX ELSE NOTHING: ')
	print('processing...')

	last_time = time()
	needle_count, optimized_matrix = generate_matrix(side_size, visability_map)
	seed = 0
	max_seed = int(str(side_size-1)*needle_count, side_size)
	print('max iterations:', max_seed)
	matrix = None

	while seed < max_seed:
		if use_random == 'y':
			matrix = complement_matrix(optimized_matrix)
		else:
			seed += 1
			matrix = complement_matrix(optimized_matrix, needle_count, seed)

		if is_viewing:
			clear()
			print(1/(time()-last_time), 'iters per second')
			last_time = time()
			for row in matrix:
				print(row)
		if check_dublicate_numbers(matrix) and check_visability_accordance(matrix, visability_map):
			break

	print('='*10)
	print(seed, 'generations in', time()-last_time, 's')
	if seed == max_seed:
		print('NO RESULT')
	else:
		for el in matrix:
			print(el)
