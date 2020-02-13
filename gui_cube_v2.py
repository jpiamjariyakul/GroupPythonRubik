import PySimpleGUI as sg
import random

import cubeGen_scramble as scramble
import cubeGen_display as cubeDisplay
import cubeGen_getNew as getNew

import solve_kocSolve as kocSolve
from variables import dict_faceColor

import imgParse_camColor as camColor

import time
from copy import deepcopy

import mainCamera

sg.theme("Reddit")

CUBE_SIZE = 20
FACE_SIZE = CUBE_SIZE * 3

# For testing purposes - obtains new cube (scrambling optional)\
def windowDefine():
	# Define frames & its individual internal components
	frame_cam_input = [
		[	sg.Text("Click to run cameras", key="_textRunCam_"),
			sg.Button("Get", key="_get_"),
			sg.Button("Confirm", key="_confirm_", disabled=True)
			] ]
	frame_cam_img = [[	sg.Column([
							[sg.Image(filename='', key='frame_0', size=(300, 300))],
							[sg.Image(filename='', key='frame_1', size=(300, 300))]	
							])	]]
	frame_cam = [	[	sg.Column([	[sg.Frame('', frame_cam_input)],
									[sg.Frame('', frame_cam_img)]	]	)	]	]

	frame_cube =	[
			[	sg.Graph((400, 400), (0, 180), (240, 0), pad=(20, 20), key="_net_", change_submits=True, drag_submits=False),
				sg.Listbox(key="_listMoves_", values=[], size=(4, 8), disabled=True)
				],
			[	sg.Text("Index: "), sg.Text("?", key="_moveIndex_", size=(3, 1)),
				sg.Slider(key="_movesProgress_", orientation="horizontal", disable_number_display=True, disabled=True, range=(0, 0), enable_events=True),
				sg.Text("Current Move: "), sg.Text("?", key="_moveCurrent_", size=(4, 1))]
		]
	frame_button_bottom = [	[	sg.Button("Solve", disabled=True, key="_solve_"),
								sg.Button("Fill"), sg.Button("Reset"), sg.Button("Cancel")
								]	]
	# Given defined frames, define layout of window
	layout = [	[	sg.Frame("Howdy", frame_cam),
					sg.Column(	[	[sg.Frame("Net Representation", frame_cube)],
									[sg.Frame("button_bottom", frame_button_bottom)]
								])
				]	]
	def graphDefine(window):
		#g = window["_net_"]
		for face_row in range(3):
			for face_col in range(4):
				if (face_col == 1) or (face_row == 1):
					window["_net_"].draw_rectangle(	(	(face_col * FACE_SIZE), 
											(face_row * FACE_SIZE)	),
										(	((face_col * FACE_SIZE) + FACE_SIZE), 
											((face_row * FACE_SIZE) + FACE_SIZE)	),
										line_color="black"
									)
		#return g
	window = sg.Window("Window Title", layout,finalize=True)
	graphDefine(window)
	return window # , g

def drawCubelets(window, cube):
	for face in range(6):
		dict_coordFace = {	0: (1, 0),
							1: (2, 1),
							2: (1, 1),
							3: (1, 2),
							4: (0, 1),
							5: (3, 1)	}
		coordFace = dict_coordFace.get(face)
		for cube_row in range(3):
			for cube_col in range(3):
				dict_colorAbbrev = {	'W': "white",
										'R': "red",
										'O': "orange",
										'Y': "yellow",
										'G': "green",
										'B': "blue"		}
				colorCube = dict_colorAbbrev.get(dict_faceColor.get(cube[face][cube_row][cube_col]))
				window["_net_"].draw_rectangle(	(	(FACE_SIZE * coordFace[0]) + (cube_col * CUBE_SIZE), 
										(FACE_SIZE * coordFace[1]) + (cube_row * CUBE_SIZE)	),
									(	(FACE_SIZE * coordFace[0]) + ((cube_col * CUBE_SIZE) + CUBE_SIZE), 
										(FACE_SIZE * coordFace[1]) + ((cube_row * CUBE_SIZE) + CUBE_SIZE)	),
									fill_color=colorCube
								)


def main(isRunningCam = False):
	#print("Making window")
	window = windowDefine()
	#cubeObtained = False
	while True: # State 1 - Waiting to initialise camera
		event, values = window.read()
		if event in (None, "Cancel"):
			break
		if event in ("_get_"):
			window["_textRunCam_"].update("Howdy bitches")
			window["_get_"].update(disabled=True)
			window["_confirm_"].update(disabled=False)
			break

	cap_0, cap_1 = camColor.cam_initCap()

	while True: # State 2 - running camera
		event, values = window.read(timeout=0, timeout_key='timeout')

		result_raw, result_combined, result_color = camColor.cam_obtain(cap_0, cap_1)
		imgbytes = (	camColor.cam_getImgbytes(result_combined[0]),
						camColor.cam_getImgbytes(result_combined[1])	)
		window['frame_0'].update(data=imgbytes[0])
		window['frame_1'].update(data=imgbytes[1])
		if event in (None, "Cancel"):
			break

		if event in ("Reset"):
			window.close()
			window = windowDefine()
		elif event in ("_confirm_"):
			camColor.cam_releaseCap(cap_0, cap_1) # Releases OCV once done
			break
			
	cubelets = mainCamera.cam_obtainCubelets(result_combined, result_color)
	cubeDisplay.printCube(cubelets)

	cube = getNew.obtainVirCube(20) # Debug purposes - generates new cube
	drawCubelets(window, cube)
	window["_confirm_"].update(disabled=True)
	ls_kocSolve, str_kocSolve = kocSolve.solveCubeKoc(kocSolve.parseCubeString(cube))
	window["_listMoves_"].update(disabled=False, values=str_kocSolve)
	print(ls_kocSolve)
	window["_movesProgress_"].update(disabled=False, range=(0, len(str_kocSolve)))
	window["_solve_"].update(disabled=False)
	cubeDisplay.printCube(cube)

	while True: # State 3 - Cube captures, spitting moves + allowing motor movement
		event, values = window.read(timeout=0, timeout_key='timeout')
		if event in (None, "Cancel"):
			break

		if event in ("_movesProgress_"): # Displays cube changes throughout the solving algorithm
			# Given valid slider values & is changing position
			# Assumes cube is obtained & kociemba moves are valid
			cube_disp = deepcopy(cube)

			# If position is 0, show default
			# If position is 1, show [0]
			# If position is 2, show [0] + [1]
			# ...

			indexMove = int(values["_movesProgress_"]) # Given float value of slider
			window["_moveIndex_"].update(str(indexMove))
			window["_moveCurrent_"].update("None")
			if (indexMove > 0): # Considers moves beyond default cube
				window["_moveCurrent_"].update(str(str_kocSolve[indexMove - 1]))
				for moveCurrent in range(indexMove):
					for i in range(ls_kocSolve[moveCurrent][1]):
						cube_disp = scramble.moveFace(ls_kocSolve[moveCurrent][0], cube_disp)
			drawCubelets(window, cube_disp)
		elif event in ("_solve_"):
			# Once in this event, no termination permitted until solving is finished
			#print(ls_kocSolve)
			window["_movesProgress_"].update(disabled=True)
			window["_solve_"].update(disabled=True)
			drawCubelets(window, cube)
			for moveCurrent in ls_kocSolve:
				#input("Solving " + moveCurrent[0])
				for i in range(moveCurrent[1]):
					cube = scramble.moveFace(moveCurrent[0], cube)
				drawCubelets(window, cube)
	window.close() # GUI loop exited - destroy window

main()