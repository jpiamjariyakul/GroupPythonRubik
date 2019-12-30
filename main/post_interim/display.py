'''
Display current state of Rubik's Cube arranged in the following formation:
   [U]
[L][F][R][B]
   [D]

Following parameters of cube:
- 3x3 standard cube
- 6 faces
'''

def printCube(cube):
	gap = 18 * " "
	print(gap + str(cube[0][0]))
	print(gap + str(cube[0][1]))
	print(gap + str(cube[0][2]))
	print(17 * " " + + 17 * "-")
	print(str(cube[4][0]) + " | " + str(cube[2][0]) + " | " + str(cube[1][0]) + " | " + str(cube[5][0]))
	print(str(cube[4][1]) + " | " + str(cube[2][1]) + " | " + str(cube[1][1]) + " | " + str(cube[5][1]))
	print(str(cube[4][2]) + " | " + str(cube[2][2]) + " | " + str(cube[1][2]) + " | " + str(cube[5][2]))
	print(17 * " " + + 17 * "-")
	print(gap + str(cube[3][0]))
	print(gap + str(cube[3][1]))
	print(gap + str(cube[3][2]))