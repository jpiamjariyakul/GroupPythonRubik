import kociemba
#import cube_gen.obtain_new as obtain_new
import display as display

# Parses cube list (including debug-generated) into single string
# In order of Kociemba faces
def parseCubeString(cube):
	str_cube = ""
	for face in range(6):
		for row in range(3):
			str_cube = str_cube + "".join(cube[face][row])
	return str_cube

# Passes cubeString to Kociemba & return solving steps
# Additionally un-parses results into list
def solveCubeKoc(str_cube):
	str_kocSolve = kociemba.solve(str_cube).split(" ")
	ls_kocSolve = []
	for moveSolve in str_kocSolve:
		if len(moveSolve) != 1:
			if moveSolve[1] == "'":
				ls_kocSolve.append((moveSolve[0], True))
			elif moveSolve[1] == "2":
				[ls_kocSolve.append((moveSolve[0], False)) for i in range(2)]
		else: ls_kocSolve.append((moveSolve, False))
	return ls_kocSolve

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

cube_test = [
	[['B', 'R', 'D'], ['F', 'U', 'U'], ['R', 'U', 'F']],
	[['U', 'R', 'R'], ['D', 'R', 'R'], ['L', 'L', 'L']],
	[['B', 'F', 'R'], ['U', 'F', 'R'], ['U', 'B', 'B']],
	[['L', 'U', 'D'], ['F', 'D', 'D'], ['D', 'D', 'F']],
	[['R', 'D', 'D'], ['B', 'L', 'L'], ['F', 'L', 'B']],
	[['F', 'B', 'U'], ['F', 'B', 'L'], ['U', 'B', 'L']]
]
display.printCube(cube_test)
str_cube = parseCubeString(cube_test)
print(str_cube)
print(printUser(solveCubeKoc(str_cube)))