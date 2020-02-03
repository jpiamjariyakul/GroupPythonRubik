import kociemba
#import cube_gen.obtain_new as obtain_new
#import displayCube

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
	str_kocSolve = kociemba.solve(str_cube).split(" ") # Removes white-spaces & places all Koc-output moves into list
	ls_kocSolve = []
	for moveSolve in str_kocSolve:
		if len(moveSolve) != 1:
			if moveSolve[1] == "'":
				ls_kocSolve.append((moveSolve[0], True))
			elif moveSolve[1] == "2":
				[ls_kocSolve.append((moveSolve[0], False)) for i in range(2)]
		else: ls_kocSolve.append((moveSolve, False))
	return ls_kocSolve, str_kocSolve