from random import randint
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

def generate_matrix(side_size, seed=None):
	if seed:
		#translate seed into side_size numeric system
		matrix = [ x for x in [ [ 0 for z in range(side_size) ] for y in range(side_size) ] ]
		matrix_expanded = []
		remains = seed
		while remains > 0 and len(matrix_expanded) < side_size**2:
			remains, number = divmod(remains, side_size)
			# разобрать пограничный случай в старшем разряде
			matrix_expanded.append(number + 1)

		for i, val in enumerate(matrix_expanded):
			hor, vert = divmod(i, side_size)
			matrix[hor][vert] = val
	
	else:
		matrix = []
		for i in range(side_size):
			row = []
			for j in range(side_size):
				row.append(randint(1, side_size))
			matrix.append(row)

	return matrix

			
					
if __name__ == '__main__':
	'''visability_map = {
		'top': [4, 4, 1, 1],
		'bottom': [1, 1, 4, 3],
		'left': [3, 4, 2, 2],
		'right': [2, 2, 3, 2],
	}

	matrix = [
		[ 0, 1, 5, 4],
		[ 1, 2, 3, 3],
		[ 2, 3, 1, 0],
		[ 3, 4, 0, 1],
	]'''
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
	#seed = int('0'*side_size**2, 4)
	seed = 0
	while True:
		if use_random == 'y':
			matrix = generate_matrix(side_size)
		else:
			seed += 1
			matrix = generate_matrix(side_size, seed)
		clear()
		if is_viewing:
			for row in matrix:
				print(row)
		if check_dublicate_numbers(matrix) and check_visability_accordance(matrix, visability_map):
			break

	for el in matrix:
		print(el)
