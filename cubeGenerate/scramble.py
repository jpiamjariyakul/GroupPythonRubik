# Valid cube scrambling algorithm
# In order of Kociemba: URFDLB
import random
from copy import deepcopy

#from . import display

# Rotates cubelets on face
def rotateStationary(face, cube_og, cube_copy):
	# Rotates top row
	cube_copy[face][0][2] = cube_og[face][0][0]
	cube_copy[face][1][2] = cube_og[face][0][1]
	cube_copy[face][2][2] = cube_og[face][0][2]
	# Rotates mid row
	cube_copy[face][0][1] = cube_og[face][1][0]
	cube_copy[face][2][1] = cube_og[face][1][2]
	# Rotates btm row
	cube_copy[face][0][0] = cube_og[face][2][0]
	cube_copy[face][1][0] = cube_og[face][2][1]
	cube_copy[face][2][0] = cube_og[face][2][2]
	return cube_copy

# Excluding opposite face, rotates all faces affected by rotation
def moveFace(face, cube):
	# Cubelets on face rotated with rotateStationary() function
	# Other faces shift their cubelets' colors
	cube_temp = deepcopy(cube)
	# Currently assumes clockwise turn
	if (face == "U"):
		# Maps B to R
		cube_temp[1][0][0] = cube[5][0][0]
		cube_temp[1][0][1] = cube[5][0][1]
		cube_temp[1][0][2] = cube[5][0][2]
		# Maps R to F
		cube_temp[2][0][0] = cube[1][0][0]
		cube_temp[2][0][1] = cube[1][0][1]
		cube_temp[2][0][2] = cube[1][0][2]
		# Maps F to L
		cube_temp[4][0][0] = cube[2][0][0]
		cube_temp[4][0][1] = cube[2][0][1]
		cube_temp[4][0][2] = cube[2][0][2]
		# Maps L to B
		cube_temp[5][0][0] = cube[4][0][0]
		cube_temp[5][0][1] = cube[4][0][1]
		cube_temp[5][0][2] = cube[4][0][2]
		# Rotates U
		cube_temp = rotateStationary(0, cube, cube_temp)
	elif (face == "R"):
		# Maps F to U
		cube_temp[0][0][2] = cube[2][0][2]
		cube_temp[0][1][2] = cube[2][1][2]
		cube_temp[0][2][2] = cube[2][2][2]
		# Maps U to B
		cube_temp[5][2][0] = cube[0][0][2]
		cube_temp[5][1][0] = cube[0][1][2]
		cube_temp[5][0][0] = cube[0][2][2]
		# Maps B to D
		cube_temp[3][0][2] = cube[5][2][0]
		cube_temp[3][1][2] = cube[5][1][0]
		cube_temp[3][2][2] = cube[5][0][0]
		# Maps D to F
		cube_temp[2][0][2] = cube[3][0][2]
		cube_temp[2][1][2] = cube[3][1][2]
		cube_temp[2][2][2] = cube[3][2][2]
		# Rotates R
		cube_temp = rotateStationary(1, cube, cube_temp)
	elif (face == "F"):
		# Maps L to U
		cube_temp[0][2][2] = cube[4][0][2]
		cube_temp[0][2][1] = cube[4][1][2]
		cube_temp[0][2][0] = cube[4][2][2]
		# Maps U to R
		cube_temp[1][0][0] = cube[0][2][0]
		cube_temp[1][1][0] = cube[0][2][1]
		cube_temp[1][2][0] = cube[0][2][2]
		# Maps R to D
		cube_temp[3][0][2] = cube[1][0][0]
		cube_temp[3][0][1] = cube[1][1][0]
		cube_temp[3][0][0] = cube[1][2][0]
		# Maps D to L
		cube_temp[4][0][2] = cube[3][0][0]
		cube_temp[4][1][2] = cube[3][0][1]
		cube_temp[4][2][2] = cube[3][0][2]
		# Rotates F
		cube_temp = rotateStationary(2, cube, cube_temp)
	elif (face == "D"):
		# Maps F to R
		cube_temp[1][2][0] = cube[2][2][0]
		cube_temp[1][2][1] = cube[2][2][1]
		cube_temp[1][2][2] = cube[2][2][2]
		# Maps R to B
		cube_temp[5][2][0] = cube[1][2][0]
		cube_temp[5][2][1] = cube[1][2][1]
		cube_temp[5][2][2] = cube[1][2][2]
		# Maps B to L
		cube_temp[4][2][0] = cube[5][2][0]
		cube_temp[4][2][1] = cube[5][2][1]
		cube_temp[4][2][2] = cube[5][2][2]
		# Maps L to F
		cube_temp[2][2][0] = cube[4][2][0]
		cube_temp[2][2][1] = cube[4][2][1]
		cube_temp[2][2][2] = cube[4][2][2]
		# Rotates D
		cube_temp = rotateStationary(3, cube, cube_temp)
	elif (face == "L"):
		# Maps B to U
		cube_temp[0][0][0] = cube[5][2][2]
		cube_temp[0][1][0] = cube[5][1][2]
		cube_temp[0][2][0] = cube[5][0][2]
		# Maps U to F
		cube_temp[2][0][0] = cube[0][0][0]
		cube_temp[2][1][0] = cube[0][1][0]
		cube_temp[2][2][0] = cube[0][2][0]
		# Maps F to D
		cube_temp[3][0][0] = cube[2][0][0]
		cube_temp[3][1][0] = cube[2][1][0]
		cube_temp[3][2][0] = cube[2][2][0]
		# Maps D to B
		cube_temp[5][2][2] = cube[3][0][0]
		cube_temp[5][1][2] = cube[3][1][0]
		cube_temp[5][0][2] = cube[3][2][0]
		# Rotates L
		cube_temp = rotateStationary(4, cube, cube_temp)
	elif (face == "B"):
		# Maps R to U
		cube_temp[0][0][2] = cube[1][2][2]
		cube_temp[0][0][1] = cube[1][1][2]
		cube_temp[0][0][0] = cube[1][0][2]
		# Maps U to L
		cube_temp[4][0][0] = cube[0][0][2]
		cube_temp[4][1][0] = cube[0][0][1]
		cube_temp[4][2][0] = cube[0][0][0]
		# Maps L to D
		cube_temp[3][2][0] = cube[4][0][0]
		cube_temp[3][2][1] = cube[4][1][0]
		cube_temp[3][2][2] = cube[4][2][0]
		# Maps D to R
		cube_temp[1][2][2] = cube[3][2][0]
		cube_temp[1][1][2] = cube[3][2][1]
		cube_temp[1][0][2] = cube[3][2][2]
		# Rotates B
		cube_temp = rotateStationary(5, cube, cube_temp)
	return cube_temp

def scramble(cube, moveCount):
	moves = ("U", "R", "F", "D", "L", "B")
	isInvert = (True, False)
	moves_done = []
	for count in range(moveCount):	
		moves_done.append((random.choice(moves), random.choice(isInvert)))
	#print(moves_done)
	moves_collated = []
	for rotation in moves_done:
		if rotation[1] == True:
			[moves_collated.append(rotation[0]) for i in range(3)]
		else:
			moves_collated.append(rotation[0])
	#print("".join(moves_collated))
	for moving in moves_collated:
		cube = moveFace(moving, cube)
		#display.printCube(cube)
	return cube
