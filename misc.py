'''
Display current state of Rubik's Cube arranged in the following formation:
   [U]
[L][F][R][B]
   [D]

Following parameters of cube:
- 3x3 standard cube
- 6 faces
'''

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