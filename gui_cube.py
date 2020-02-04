import PySimpleGUI as sg
import random

import cubeGenerate.obtainNew as obtainNew
import solving.kocSolve as kocSolve

from solving.dictColor import dict_faceColor

from copy import deepcopy

sg.theme("Reddit")
'''
cube = 	[
    [['G', 'Y', 'W'], ['W', 'B', 'W'], ['W', 'O', 'Y']], 
    [['G', 'G', 'R'], ['B', 'R', 'B'], ['O', 'R', 'W']],
    [['O', 'G', 'R'], ['O', 'W', 'R'], ['R', 'Y', 'G']],
    [['B', 'B', 'W'], ['B', 'G', 'Y'], ['Y', 'R', 'G']],
    [['Y', 'O', 'B'], ['G', 'O', 'Y'], ['O', 'W', 'Y']],
    [['B', 'G', 'O'], ['O', 'Y', 'R'], ['R', 'W', 'B']]
]
'''

CUBE_SIZE = 20
FACE_SIZE = CUBE_SIZE * 3

# For testing purposes - obtains new cube (scrambling optional)

def windowDefine():
	# Define frames & its individual internal components
	frame_input = [
		[sg.Text("Click to obtain new cube"), sg.Button("Get", key="_get_"), sg.Button("Confirm", key="_confirm_", disabled=True)]
		]
	frame_cube =	[
		[sg.Graph((400, 400), (0, 180), (240, 0), key="_net_", change_submits=True, drag_submits=False), sg.Listbox(key="_listMoves_", values=[], size=(4, 8), disabled=True)],
		[sg.Slider(key="_movesProgress_", orientation="horizontal", disabled=True, range=(0, 0))]
		]
	frame_button_bottom = [
		[sg.Button("Solve"), sg.Button("Fill"), sg.Button("Reset"), sg.Button("Cancel")]
	]
	# Given defined frames, define layout of window
	layout = [
		[sg.Frame("Test Frame", frame_input)],
		[sg.Frame("Net Representation", frame_cube)],
		[sg.Frame("button_bottom", frame_button_bottom)]
	]
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
		dict_coordFace = {
			0: (1, 0),
			1: (2, 1),
			2: (1, 1),
			3: (1, 2),
			4: (0, 1),
			5: (3, 1)
		}
		coordFace = dict_coordFace.get(face)
		for cube_row in range(3):
			for cube_col in range(3):
				dict_colorAbbrev = {
					'W': "white",
					'R': "red",
					'O': "orange",
					'Y': "yellow",
					'G': "green",
					'B': "blue"
				}
				colorCube = dict_colorAbbrev.get(dict_faceColor.get(cube[face][cube_row][cube_col]))
				window["_net_"].draw_rectangle(	(	(FACE_SIZE * coordFace[0]) + (cube_col * CUBE_SIZE), 
										(FACE_SIZE * coordFace[1]) + (cube_row * CUBE_SIZE)	),
									(	(FACE_SIZE * coordFace[0]) + ((cube_col * CUBE_SIZE) + CUBE_SIZE), 
										(FACE_SIZE * coordFace[1]) + ((cube_row * CUBE_SIZE) + CUBE_SIZE)	),
									fill_color=colorCube
								)


def main():
	window = windowDefine()
	while True:
		event, values = window.read()
		if event in (None, "Cancel"):
			break
		elif event in ("Reset"):
			window.close()
			window = windowDefine()
		elif event in ("_get_"):
			window["_get_"].update(disabled=True)
			window["_confirm_"].update(disabled=False)
		elif event in ("_confirm_"):
			cube = obtainNew.obtainVirCube(6) # Debug purposes - generates new cube
			drawCubelets(window, cube)
			window["_confirm_"].update(disabled=True)
			ls_kocSolve, str_kocSolve = kocSolve.solveCubeKoc(kocSolve.parseCubeString(cube))
			window["_listMoves_"].update(disabled=False, values=str_kocSolve)
			#print(ls_kocSolve)
			#if sz != movesStatus:
			cube_temp = deepcopy(cube)
			
			window["_movesProgress_"].update(disabled=False, range=(0, len(str_kocSolve)))
		elif event in ("Fill"):
			print("Color filled!")
		
		sz = int(values["_movesProgress_"])
		print(sz)

	window.close()

main()