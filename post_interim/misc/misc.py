'''
Display current state of Rubik's Cube arranged in the following formation:
   [U]
[L][F][R][B]
   [D]

Following parameters of cube:
- 3x3 standard cube
- 6 faces
'''

# Prints Rubik's Cube arrays into a user-friendly format on console
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

# Prints Kociemba-generated output moves into a user-friendly list
def printUser(ls_kocSolve):
	ls_user = []
	for i in ls_kocSolve:
		if i[1] == True:
			if i[0] == 'U':
				ls_user.append("UP-rev")
			elif i[0] == 'R':
				ls_user.append("RIGHT-rev")
			elif i[0] == 'F':
				ls_user.append("FRONT-rev")
			elif i[0] == 'D':
				ls_user.append("DOWN-rev")
			elif i[0] == 'L':
				ls_user.append("LEFT-rev")
			elif i[0] == 'B':
				ls_user.append("BACK-rev")
		else:
			if i[0] == 'U':
				ls_user.append("UP")
			elif i[0] == 'R':
				ls_user.append("RIGHT")
			elif i[0] == 'F':
				ls_user.append("FRONT")
			elif i[0] == 'D':
				ls_user.append("DOWN")
			elif i[0] == 'L':
				ls_user.append("LEFT")
			elif i[0] == 'B':
				ls_user.append("BACK")
	return ls_user