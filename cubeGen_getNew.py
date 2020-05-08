#import cubeGen_generate as cg_g
import cubeGen_scramble as cg_s

'''
Order of Kociemba algorithm input is in following order: URFDLB
One sets UP color as WHITE - change according to necessary

Program maps 	WHITE	to	UP
				GREEN	to	RIGHT
				ORANGE	to	FRONT
				YELLOW	to	DOWN
				BLUE	to 	LEFT
				RED		to	BACK
regarding middle cubelets
'''
# Generates full cube set, faces in URFDLB
def generate():
	ls_faces = ("U", "R", "F", "D", "L", "B")
	cubelets = []
	for face in range(len(ls_faces)):
		cubelets.append([])
		for row in range(3):
			cubelets[face].append([])
			for column in range(3):
				cubelets[face][row].append(ls_faces[face])
	return cubelets

# Generates & returns new (optionally scrambled) virtual cube
def obtainVirCube(scrambles=0):
	cubelets = generate()
	if scrambles != 0: 
		#print(isScrambled)
		cubelets = cg_s.scramble(cubelets, scrambles)
	return cubelets

#cg_d.printCube(obtainVirCube(3))
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

#printCube(obtainVirCube(4))