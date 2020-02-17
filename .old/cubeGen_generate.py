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