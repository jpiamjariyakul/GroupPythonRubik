import kociemba
import cube_gen.obtain_new as obtain_new
import cube_gen.display as display

def parseCubeString(cube):
	str_cube = ""
	for face in range(6):
		for row in range(3):
			str_cube = str_cube + "".join(cube[face][row])
	return str_cube

def solveCubeKoc(str_cube):
	str_kocSolve = kociemba.solve(str_cube).split(" ")
	return str_kocSolve


cube_test = obtain_new.obtainVirCube(True, 4)
display.printCube(cube_test)
str_cube = parseCubeString(cube_test)
print(str_cube)
print(solveCubeKoc(str_cube))