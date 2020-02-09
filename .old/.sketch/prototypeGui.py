'''
layout_1 =	[	[sg.Text('Some text on Row 1')],
				[sg.Text('Enter something on Row 2'), sg.InputText()],
				[sg.Button('Ok'), sg.Button('Cancel')]
			]
window = sg.Window('Window Title', layout_1)
while True:
	event, values = window.read()
	if event in (None, 'Cancel'):
		break
	print('You entered ', values[0])
window.close()

#sg.theme('DarkAmber')	# Add a touch of color
def wrapStage1(isNotTerminated):
	print("Stage 1 initialised")
	layout_1 =	[	[sg.Text("Stage 1 - Image Parsing & Processing")],
					[sg.Text("Click OK once cube positions are in place")],
					[sg.Text("See OpenCV windows")],
					[sg.Button("OK"), sg.Button("Next"), sg.Button("Cancel")]
				]
	window_1 = sg.Window("Stage 1", layout_1)
	while True:
		event, values = window_1.read()
		if event in (None, "Cancel"):
			isNotTerminated = False
			break
		elif event in (None, "Next"):
			break
		elif event in (None, "OK"):
			print("OK Clicked")
	window_1.close()
	return isNotTerminated

def wrapStage2(isNotTerminated):
	print("Stage 2 initialised")
	layout_2 =	[	[sg.Text("Stage 2 - Solving Algorithm", key="_test_")],
					[sg.Text("Click OK once cube positions are in place")],
					[sg.Text("See OpenCV windows")],
					[sg.Button("OK"), sg.Button("Next"), sg.Button("Cancel")]
				]
	window_2 = sg.Window("Stage 2", layout_2)
	while True:
		event, values = window_2.read()
		if event in (None, "Cancel"):
			isNotTerminated = False
			break
		elif event in (None, "Next"):
			break
		elif event in (None, "OK"):
			print("OK Clicked")
			window_2["_test_"].update("Hello!")
	window_2.close()
	return isNotTerminated

def main():
	isNotTerminated = True
	while (isNotTerminated == True):
		isNotTerminated = wrapStage1(isNotTerminated)
		break
	while (isNotTerminated == True):
		isNotTerminated = wrapStage2(isNotTerminated)
		break

main()

'''

'''
frame_1 = 	[	[sg.Text('Text inside of a frame', key="_test_")],
				[sg.Checkbox('Check 1'), sg.Checkbox('Check 2')],
			]
frame_2 =	[	[sg.Text('Text inside another frame')],
				[sg.Text('Hello!'), sg.Button("OK"), sg.Button("Cancel")]
			]
frame_3 =	[	[sg.Text("Third frame's a charm!")],
				[sg.Text("End of the frame")]
			]

layout = 	[	
				[sg.Frame("Title of Frame 1", frame_1), sg.Frame("Title of Second Frame", frame_2)],
				[sg.Frame("Frame the Third", frame_3)]
			]
'''

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
    [sg.Button("Fill"), sg.Button("Cancel")]
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

