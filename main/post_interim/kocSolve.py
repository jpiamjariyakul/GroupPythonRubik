import kociemba
#import cube_gen.obtain_new as obtain_new

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
	for moveSolve in str_kocSolve: # Loops over all items in the Koc output string (sans the white-spaces)
        # Checks if it's just a single character in list or two
		if len(moveSolve) != 1: # If there's a second character i.e. single-quote or '2'
			if moveSolve[1] == "'": # single-quote indicates counter-clockwise turn
				ls_kocSolve.append((moveSolve[0], True)) # Appends 'True' to position [1] of (,) since inverted
			elif moveSolve[1] == "2": # '2' indicates twice turn
				[ls_kocSolve.append((moveSolve[0], False)) for i in range(2)] # Simply outputs face-turn & False (since not inverted turn)
                # Outputs twice since it's a double turn
		else: ls_kocSolve.append((moveSolve, False)) # Simply outputs face-turn & False
	return ls_kocSolve