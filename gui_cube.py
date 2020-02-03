import PySimpleGUI as sg
import random

cube = 	[
    [['G', 'Y', 'W'], ['W', 'B', 'W'], ['W', 'O', 'Y']], 
    [['G', 'G', 'R'], ['B', 'R', 'B'], ['O', 'R', 'W']],
    [['O', 'G', 'R'], ['O', 'W', 'R'], ['R', 'Y', 'G']],
    [['B', 'B', 'W'], ['B', 'G', 'Y'], ['Y', 'R', 'G']],
    [['Y', 'O', 'B'], ['G', 'O', 'Y'], ['O', 'W', 'Y']],
    [['B', 'G', 'O'], ['O', 'Y', 'R'], ['R', 'W', 'B']]
]

CUBE_SIZE = 20
FACE_SIZE = CUBE_SIZE * 3

frame_input = [
	[sg.Text("Click to test"), sg.Button("Get")]
	]
frame_cube =	[
	[sg.Graph((400, 400), (0, 180), (240, 0), key='-GRAPH-', change_submits=True, drag_submits=False)],
	[sg.Slider(orientation="horizontal", range=(1, 20))]
	]
layout = [
    [sg.Text("Rubik's Cube Solver GUI Prototype")], #, sg.Text('', key='-OUTPUT-')],
	[sg.Frame("Test Frame", frame_input)],
    [sg.Frame("Net Representation", frame_cube)],
    [sg.Button("Solve"), sg.Button("Fill"), sg.Button("Cancel")]
]

window = sg.Window("Window Title", layout, finalize=True)
g = window["-GRAPH-"]

def returnFaceCoord(face):
	if face == 0: return (1, 0)
	elif face == 1: return (2, 1)
	elif face == 2: return (1, 1)
	elif face == 3: return (1, 2)
	elif face == 4: return (0, 1)
	elif face == 5: return (3, 1)

for face_row in range(3):
	for face_col in range(4):
		if (face_col == 1) or (face_row == 1):
			g.draw_rectangle(	(	(face_col * FACE_SIZE), 
									(face_row * FACE_SIZE)	),
								(	((face_col * FACE_SIZE) + FACE_SIZE), 
									((face_row * FACE_SIZE) + FACE_SIZE)	),
								line_color="black", line_width=4
							)

while True:
	event, values = window.read()
	if event in (None, "Cancel"):
		break
	elif event in (None, "Fill"):
		for face in range(6):
			coordFace = returnFaceCoord(face)
			for cube_row in range(3):
				for cube_col in range(3):
					cubeCurrent = cube[face][cube_row][cube_col]
					if 		(cubeCurrent == 'W'): 	colorCube = "white"
					elif	(cubeCurrent == 'R'): 	colorCube = "red"
					elif 	(cubeCurrent == 'O'): 	colorCube = "orange"
					elif 	(cubeCurrent == 'Y'): 	colorCube = "yellow"
					elif 	(cubeCurrent == 'G'): 	colorCube = "green"
					elif 	(cubeCurrent == 'B'): 	colorCube = "blue"
					g.draw_rectangle(	(	(FACE_SIZE * coordFace[0]) + (cube_col * CUBE_SIZE), 
											(FACE_SIZE * coordFace[1]) + (cube_row * CUBE_SIZE)	),
										(	(FACE_SIZE * coordFace[0]) + ((cube_col * CUBE_SIZE) + CUBE_SIZE), 
											(FACE_SIZE * coordFace[1]) + ((cube_row * CUBE_SIZE) + CUBE_SIZE)	),
										fill_color=colorCube, line_width=1
									)
		print("Color filled!")

window.close()

