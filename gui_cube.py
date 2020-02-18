import time
from copy import deepcopy
import random

import PySimpleGUI as sg

import cubeGen_scramble as scramble
#import cubeGen_display as cubeDisplay
import cubeGen_getNew as getNew

import solve_cubeSolve as cubeSolve
from variables import dict_faceColor

import solve_getAscii as getAscii

import imgParse_getColor as getColor
import imgParse_initCam as initCam

import audio_waveSine as waveSine
import pygame

CUBE_SIZE = 20
FACE_SIZE = CUBE_SIZE * 3

# For testing purposes - obtains new cube (scrambling optional)\
def windowDefine():
	sg.theme("Reddit")
	# Define frames & its individual internal components
	frame_input_cam = [	[	sg.Radio("Camera Input", "Radio_Input", True, key="_radio_cam_")
							],
						[	sg.Text("Click to run cameras", key="_textRunCam_", auto_size_text=True),
							sg.Button("Get", key="_input_cam_"),
							sg.Button("Confirm", key="_confirm_cam_", disabled=True)
							],
						[	sg.Column([	[	sg.Image(filename='', key="frame_raw_0", size=(200, 200)), 
											sg.Image(filename='', key="frame_combined_0", size=(200, 200))
											],
										[	sg.Image(filename='', key="frame_raw_1", size=(200, 200)),
											sg.Image(filename='', key="frame_combined_1", size=(200, 200))
											]
										])
							]
						]
	frame_input_ascii =	[	[	sg.Radio("ASCII File Input", "Radio_Input", key="_radio_ascii_")
								],
							[	sg.Text("Browse for text file containing moves", auto_size_text=True)	
								],
							[	sg.Input(key="_file_ascii_"), sg.FileBrowse(key="_input_file_"),
								sg.Button("Confirm", key="_confirm_file_")
								],
							]
	frame_cube =	[	[	sg.Graph((400, 400), (0, 180), (240, 0), pad=(20, 20), key="_net_", change_submits=True, drag_submits=False),
							sg.Listbox(key="_listMoves_", values=[], size=(4, 8), disabled=True)
							],
						[	sg.Text("Index: "), sg.Text("?", key="_moveIndex_", size=(3, 1)),
							sg.Slider(key="_movesProgress_", orientation="horizontal", disable_number_display=True, disabled=True, range=(0, 0), enable_events=True),
							sg.Text("Current Move: "), sg.Text("?", key="_moveCurrent_", size=(4, 1))
							]
						]
	frame_button_bottom = 	[	[	sg.Button("Solve/Mix", disabled=True, key="_solve_"),
									sg.Button("Reset", key="_reset_"), sg.Button("Terminate", key="_terminate_")
									]
								]
	# Given defined frames, define layout of window
	layout = 	[	[	sg.Column(	[	[sg.Frame("Camera Input", frame_input_cam)],
										[sg.Frame("ASCII Input", frame_input_ascii)]
									]),
						sg.Column(	[	[sg.Frame("Net Representation", frame_cube)],
										[sg.Frame("Control", frame_button_bottom)]
									])
						]
					]
	def graphDefine(window):
		for face_row in range(3):
			for face_col in range(4):
				if (face_col == 1) or (face_row == 1):
					window["_net_"].draw_rectangle(	(	(face_col * FACE_SIZE), 
											(face_row * FACE_SIZE)	),
										(	((face_col * FACE_SIZE) + FACE_SIZE), 
											((face_row * FACE_SIZE) + FACE_SIZE)	),
										line_color="black"
									)
	window = sg.Window("Window Title", layout, finalize=True, return_keyboard_events=True, use_default_focus=False)
	graphDefine(window)
	return window

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


def main(): # Implements each stage of GUI progression with state machine
	# Defines state machine verification
	ls_state = [	"INIT", 
					"CAM_IDLE", "CAM_GET", "CAM_SET",
					"ASC_IDLE", "ASC_GET", "ASC_SET",
					"MOVES_GET_CAM", "MOVES_GET_ASC",
					"MOVES_SET", "MOVES_RUN", "DONE"	]
	st_Prev, st_Curr = "DONE", "INIT" # Defines startup states

	window = windowDefine() # Sets window to defined layout
	while True: 
		# Reads events & values in window, provided certain small update & delay
		event, values = window.read(timeout=0, timeout_key='timeout')
		if (st_Curr != st_Prev):
			print("States: " + st_Curr + ", " + st_Prev)

		## Global events - applicable to all states (given user being able to input)
		if event in (None, "_terminate_"): # Given cancel clicked, exits program
			break
		if event in ("_reset_"): # Given reset clicked, goes back to initial state
			window.close()
			window = windowDefine()
			st_Curr = "INIT"
			#print("States: " + st_Curr + ", " + st_Prev)

		# Prototype - input with keyboard
		# if event != "timeout":
		# 	print(event)

		## Program only runs if states are in list of valid states
		if (st_Prev in ls_state) and (st_Curr in ls_state):
			###	Given launch, waits for user input to method of obtaining moves
			if st_Curr == "INIT": # State: Idle-waiting to initialise camera
				if (st_Curr != st_Prev): # Should not enter here if working properly
					window["_input_file_"].update(disabled=True)
					window["_confirm_file_"].update(disabled=True)
					window["_file_ascii_"].update(disabled=True)
					window["_input_cam_"].update(disabled=True)
					window["_confirm_cam_"].update(disabled=True)
					window["_radio_ascii_"].update(disabled=False)
					window["_radio_cam_"].update(disabled=False)
					st_Prev = st_Curr #  _radio_ascii_
				if values["_radio_cam_"]:
					st_Curr = "CAM_IDLE"
				if values["_radio_ascii_"]:
					st_Curr = "ASC_IDLE"
			
			## ------------------------------------------------------------------------
			## Concerns camera-related inputs
			if st_Curr == "CAM_IDLE":
				if (st_Curr != st_Prev):
					window["_input_cam_"].update(disabled=False)
					st_Prev = st_Curr
				window["frame_raw_0"].update(data=None)
				window["frame_raw_1"].update(data=None)
				window["frame_combined_0"].update(data=None)
				window["frame_combined_1"].update(data=None)
				if event in ("_input_cam_"):
					st_Curr = "CAM_GET"
				if values["_radio_ascii_"]:
					st_Curr = "INIT"
			###	Given request, sets up camera to obtain images
			elif st_Curr == "CAM_GET": # State: Runs cameras & obtains pictures
				if (st_Curr != st_Prev): # Should come from "INIT"
					window["_input_cam_"].update(disabled=True)
					window["_confirm_cam_"].update(disabled=False)
					window["_textRunCam_"].update("Press [CONFIRM] to confirm camera input")
					cap_0, cap_1 = getColor.cam_initCap()
					st_Prev = st_Curr
				result_raw, result_combined, result_color = getColor.cam_obtain(cap_0, cap_1)
				imgbytes_raw = (	getColor.cam_getImgbytes(result_raw[0], 200	),
									getColor.cam_getImgbytes(result_raw[1], 200	)	)
				imgbytes_combined = (	getColor.cam_getImgbytes(result_combined[0], 200	),
										getColor.cam_getImgbytes(result_combined[1], 200	)	)
				window["frame_raw_0"].update(data=imgbytes_raw[0])
				window["frame_raw_1"].update(data=imgbytes_raw[1])
				window["frame_combined_0"].update(data=imgbytes_combined[0])
				window["frame_combined_1"].update(data=imgbytes_combined[1])
				if event in ("_confirm_cam_"):
					st_Curr = "CAM_SET"
				elif event in ("_reset_"):
					getColor.cam_releaseCap(cap_0, cap_1)
					window["frame_raw_0"].update(data=None)
					window["frame_raw_1"].update(data=None)
					window["frame_combined_0"].update(data=None)
					window["frame_combined_1"].update(data=None)
				if values["_radio_ascii_"]:
					getColor.cam_releaseCap(cap_0, cap_1)
					st_Curr = "INIT"
			###	Given camera confirmation, obtains cubelets from such images
			elif st_Curr == "CAM_SET":
				st_Prev = st_Curr
				window["_confirm_cam_"].update(disabled=True)
				getColor.cam_releaseCap(cap_0, cap_1) # Releases OCV once done
				cubelets = initCam.cam_obtainCubelets(result_combined, result_color)
				getNew.printCube(cubelets)
				cube = getNew.obtainVirCube(50) # Debug purposes - generates new cube
				# Replace above line w/ verification of camera-obtained cubelet
				st_Curr = "MOVES_GET_CAM"
			###	Given cube parsed from images, evaluates moves from camera
			elif st_Curr == "MOVES_GET_CAM":
				st_Prev = st_Curr
				ls_kocSolve, str_kocSolve = cubeSolve.solveCubeKoc(cubeSolve.parseCubeString(cube))
				ls_runMoves, str_runMoves = ls_kocSolve, str_kocSolve
				print(ls_runMoves)
				getNew.printCube(cube)
				st_Curr = "MOVES_SET"

			## ------------------------------------------------------------------------
			## Refers to ASCII-related inputs
			elif st_Curr == "ASC_IDLE":
				st_Prev = st_Curr
				window["frame_raw_0"].update(data=None)
				window["frame_raw_1"].update(data=None)
				window["frame_combined_0"].update(data=None)
				window["frame_combined_1"].update(data=None)
				st_Curr = "ASC_GET"
			elif st_Curr == "ASC_GET":
				if (st_Curr != st_Prev):
					window["_confirm_file_"].update(disabled=False)
					window["_input_file_"].update(disabled=False)
					window["_file_ascii_"].update(disabled=False)
					st_Prev = st_Curr
				if event in ("_confirm_file_"): #f=open("guru99.txt", "r")
					st_Curr = "ASC_SET"
				if values["_radio_cam_"]:
					st_Curr = "INIT"
			elif st_Curr == "ASC_SET":
				st_Prev = st_Curr
				window["_confirm_file_"].update(disabled=True)
				window["_input_file_"].update(disabled=True)
				window["_file_ascii_"].update(disabled=True)
				fileMixup = open(str(values["_file_ascii_"]), 'r')
				str_Mixup = fileMixup.read()
				st_Curr = "MOVES_GET_ASC"
			elif st_Curr == "MOVES_GET_ASC":
				st_Prev = st_Curr
				str_ascii = getAscii.returnParsedStr(str_Mixup) # Test list of moves
				ls_ascii = cubeSolve.getMovesList(str_ascii)
				ls_runMoves, str_runMoves = ls_ascii, str_ascii
				cube = getNew.obtainVirCube()
				st_Curr = "MOVES_SET"

				
			## ------------------------------------------------------------------------
			###	Given set of moves, prep program to run moves, including simulation
			elif st_Curr == "MOVES_SET":
				if (st_Curr != st_Prev): # Should come from "CAM_SET"
					window["_radio_ascii_"].update(disabled=True)
					window["_radio_cam_"].update(disabled=True)
					drawCubelets(window, cube)
					window["_listMoves_"].update(disabled=False, values=str_runMoves)
					window["_movesProgress_"].update(disabled=False, range=(0, len(str_runMoves)), value=0)
					window["_solve_"].update(disabled=False)
					window["_moveCurrent_"].update("None")
					window["_moveIndex_"].update(0)
					st_Prev = st_Curr
				''' Given input into slider, simulates cube turning
				'''
				if event in ("_movesProgress_"): # Displays cube changes throughout the solving algorithm
					# Given valid slider values & is changing position
					# Assumes cube is obtained & kociemba moves are valid
					# I.E.
					# If position is 0, show initial
					# If position is 1, show [0]
					# If position is 2, show [0] + [1]
					# ...
					cube_disp = deepcopy(cube)
					indexMove = int(values["_movesProgress_"]) # Given float value of slider
					window["_moveIndex_"].update(str(indexMove))
					window["_moveCurrent_"].update("None")
					if (indexMove > 0): # Considers moves beyond default cube
						window["_moveCurrent_"].update(str(str_runMoves[indexMove - 1]))
						for moveCurrent in range(indexMove):
							for i in range(ls_runMoves[moveCurrent][1]):
								cube_disp = scramble.moveFace(ls_runMoves[moveCurrent][0], cube_disp)
					drawCubelets(window, cube_disp)
				elif event in ("_solve_"):
					# Once in this event, no termination permitted until solving is finished
					st_Curr = "MOVES_RUN"

			###	Given user confirmation to run moves, runs such moves
			elif st_Curr == "MOVES_RUN":
				if (st_Curr != st_Prev): # Should come from "MOVES_SET"
					window["_movesProgress_"].update(disabled=True)
					window["_solve_"].update(disabled=True)
					drawCubelets(window, cube)
				for index in range(len(ls_runMoves)):
					moveCurrent = ls_runMoves[index]
					window["_movesProgress_"].update(value=(index + 1))
					window["_moveIndex_"].update(str(index + 1))
					window["_moveCurrent_"].update(str(str_runMoves[index]))
					#print(index + 1)
					for i in range(moveCurrent[1]):
						cube = scramble.moveFace(moveCurrent[0], cube)
						# TODO: Audio - output per file
						waveSine.audioInputSeq(moveCurrent[0])
					drawCubelets(window, cube)
					window.refresh()
				st_Curr = "DONE"

			### Given move completion, affirm with message
			elif st_Curr == "DONE":
				if (st_Curr != st_Prev): # Should come from "MOVES_RUN"
					print("DONE!")
					st_Prev = st_Curr
				st_Curr = "INIT"
				
			else: # Given invalid state
				print("Invalid state! - Exiting")
				break
		else: # Given invalid state
			print("Invalid state! - Exiting")
			break
	window.close() # GUI loop exited - destroy window

if __name__ == "__main__":
	main()