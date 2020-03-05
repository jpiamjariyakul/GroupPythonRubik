# System & installed modules
from copy import deepcopy
import PySimpleGUI as sg
import pygame

# Importing specific variables to be utilised in GUI
from variables import dict_faceColor

# Custom modules to obtain functions necessary
import cubeGen_scramble as scramble
import cubeGen_getNew as getNew
import solve_cubeSolve as cubeSolve
import solve_getAscii as getAscii
import imgParse_getColor as getColor
import imgParse_initCam as initCam
import audio_waveSine as waveSine
# NB: Not importing everything - only entry-point functions required to operate GUI

# Draws outline of cube faces & (if specified) individual cubelets
def drawCubelets(window, cube=[]):
	CUBE_SIZE = 20
	FACE_SIZE = CUBE_SIZE * 3
	for face_row in range(3): # Draws empty faces - three rows in net representaiton
		for face_col in range(4): # Four columns in net representation
			if (face_col == 1) or (face_row == 1): # Draws outlines given cross-like structure
				window["_net_"].draw_rectangle(	(	(face_col * FACE_SIZE), 
													(face_row * FACE_SIZE)
													),
												(	((face_col * FACE_SIZE) + FACE_SIZE), 
													((face_row * FACE_SIZE) + FACE_SIZE)
													),
												line_color="black", fill_color="white"
												)
	if (cube != []): # If cube parameter passed, draw colored cubelets as well
		for face in range(6):
			dict_coordFace = {	0: (1, 0), 1: (2, 1),
								2: (1, 1), 3: (1, 2),
								4: (0, 1), 5: (3, 1)	}
			coordFace = dict_coordFace.get(face)
			for cube_row in range(3):
				for cube_col in range(3):
					dict_colorAbbrev = {	'W': "white",	'R': "red",
											'O': "orange",	'Y': "yellow",
											'G': "green",	'B': "blue"		}
					colorCube = dict_colorAbbrev.get(dict_faceColor.get(cube[face][cube_row][cube_col]))
					window["_net_"].draw_rectangle(	(	(FACE_SIZE * coordFace[0]) + (cube_col * CUBE_SIZE), 
														(FACE_SIZE * coordFace[1]) + (cube_row * CUBE_SIZE)	
														),
													(	(FACE_SIZE * coordFace[0]) + ((cube_col * CUBE_SIZE) + CUBE_SIZE), 
														(FACE_SIZE * coordFace[1]) + ((cube_row * CUBE_SIZE) + CUBE_SIZE)
														),
													fill_color=colorCube
													)

# Defines layout of GUI to be displayed - some initial values are assigned here
def windowDefine():
	sg.theme("Reddit") # Reddit theme applied (no orange, though - sad)
	# Define frames & its individual internal components
	frame_in_cam = [	[	sg.Radio("Camera Input", "Radio_Input", True, key="_radio_cam_"),
							sg.Button("Run/Confirm", key="_btn_inputCam_")
							],
						# Image components to display OpenCV outputs (including raw & processed frames)
						[	sg.Column([	[	sg.Image(filename='', key="frame_raw_0", background_color="black", pad=(5, 5)), 
											sg.Image(filename='', key="frame_combined_0", background_color="black", pad=(5, 5))
											],
										[	sg.Image(filename='', key="frame_raw_1", background_color="black", pad=(5, 5)),
											sg.Image(filename='', key="frame_combined_1", background_color="black", pad=(5, 5))
											]
										])
							]
						]
	frame_in_ascii =	[	[	sg.Radio("ASCII File Input", "Radio_Input", key="_radio_ascii_")
								],
							[	sg.Text("Browse for text file containing moves", auto_size_text=True)	
								],
							[	sg.Input(key="_file_ascii_"), sg.FileBrowse(key="_btn_inputFile_"),
								sg.Button("Confirm", key="_btn_confirmFile_")
								],
							]
	frame_in_manual = [	[	sg.Radio("Manual Movement Input", "Radio_Input", key="_radio_manual_")
							],
						# Buttons to control face to rotate & drop-down list to select direction/mode
						[	sg.Button("UP", key="_btn_man_U_"), sg.Button("RIGHT", key="_btn_man_R_"), sg.Button("FRONT", key="_btn_man_F_"), 
							sg.Button("DOWN", key="_btn_man_D_"), sg.Button("LEFT", key="_btn_man_L_"), sg.Button("BACK", key="_btn_man_B_"),
							sg.DropDown(values=["Forward", "Double", "Reverse"], key="_ls_mnl_mode_", default_value="Forward", readonly=True)
							]
						]
	# Frame containing display of cube's net representation output
	frame_cube =	[	[	sg.Text("Index: "), sg.Text("?", key="_txt_moveIndex_", size=(3, 1)),
							sg.Slider(key="_slide_movesProgress_", orientation="horizontal", disable_number_display=True, disabled=True, range=(0, 0), enable_events=True),
							sg.Text("Current Move: "), sg.Text("?", key="_txt_moveCurrent_", size=(4, 1))
							],
						# Canvas/graph that contains the representation itself, alongside list to display moves
						[	sg.Graph((400, 400), (0, 180), (240, 0), pad=(20, 20), key="_net_", change_submits=True, drag_submits=False),
							sg.Listbox(key="_listMoves_", values=[], size=(4, 8), disabled=True)
							]
						]
	frame_btn_ctrl = 	[	[	sg.Button("Solve/Mix", disabled=True, key="_btn_solve_"),
								sg.Button("Reset", key="_btn_reset_"),
								sg.Button("Terminate", key="_btn_terminate_")
								]
							]
	# Given defined frames, define layout of window - separated into two columns
	layout = 	[	[	sg.Column(	[	[sg.Frame("Camera Input Mode", frame_in_cam)],
										[sg.Frame("ASCII Input Mode", frame_in_ascii)]
									]),
						sg.Column(	[	[sg.Frame("Manual Input Mode", frame_in_manual)],
										[sg.Frame("Net Representation", frame_cube)],
										[sg.Frame("Control Unit", frame_btn_ctrl)]
									])
						]
					]
	window = sg.Window("Window Title", layout, finalize=True, return_keyboard_events=True, use_default_focus=False)
	return window

if __name__ == "__main__": # Implements each stage of GUI progression with state machine
	# Defines state machine verification
	ls_state = [	"INIT", 
					"CAM_IDLE", "CAM_GET", "CAM_SET",
					"ASC_IDLE", "ASC_GET", "ASC_SET",
					"MOVES_GET_CAM", "MOVES_GET_ASC",
					"MOVES_SET", "MOVES_RUN",
					"DONE",
					"MNL_IDLE", "MNL_GET", "MNL_SET"
					]
	st_Prev, st_Curr = "DONE", "INIT" # Defines startup states

	window = windowDefine() # Sets window to defined layout
	while True: 
		# Reads events & values in window, provided certain small update & delay
		event, values = window.read(timeout=0, timeout_key='timeout')
		# Given current state != previous state, output states to console log
		if (st_Curr != st_Prev): print("States: " + st_Curr + ", " + st_Prev)

		## Global events - applicable to all states (given user being able to input)
		if event in (None, "_btn_terminate_"): # Given cancel clicked, exits program
			break
		if event in ("_btn_reset_"): # Given reset clicked, goes back to initial state
			st_Curr = "INIT"
			if ("cap_0" in locals()) or  ("cap_1" in locals()): getColor.cam_releaseCap(cap_0, cap_1)
			window.close()
			window = windowDefine()

		## Program only runs if states are in list of valid states
		if (st_Prev in ls_state) and (st_Curr in ls_state):
			###	Given launch, waits for user input to method of obtaining moves
			if st_Curr == "INIT": # State: Idle-waiting to initialise camera
				window["_radio_ascii_"].update(disabled=False)
				window["_file_ascii_"].update(disabled=True)
				window["_btn_inputFile_"].update(disabled=True)
				window["_btn_confirmFile_"].update(disabled=True)

				window["_radio_cam_"].update(disabled=False)
				window["_btn_inputCam_"].update(disabled=True)
				window["frame_raw_0"].update(filename='', size=(200, 200))
				window["frame_raw_1"].update(filename='', size=(200, 200))
				window["frame_combined_0"].update(filename='', size=(200, 200))
				window["frame_combined_1"].update(filename='', size=(200, 200))
				#window["_btn_confirmCam_"].update(disabled=True)

				window["_radio_manual_"].update(disabled=False)
				window["_btn_man_U_"].update(disabled=True)
				window["_btn_man_R_"].update(disabled=True)
				window["_btn_man_F_"].update(disabled=True)
				window["_btn_man_D_"].update(disabled=True)
				window["_btn_man_L_"].update(disabled=True)
				window["_btn_man_B_"].update(disabled=True)
				window["_ls_mnl_mode_"].update(disabled=True)

				window["_listMoves_"].update(disabled=True, values=None)
				window["_slide_movesProgress_"].update(disabled=True, range=(0, 0), value=0)
				window["_txt_moveCurrent_"].update("?")
				window["_txt_moveIndex_"].update("?")
				drawCubelets(window) # Draws empty faces on net grid

				if values["_radio_cam_"]:		st_Curr = "CAM_IDLE"
				if values["_radio_ascii_"]:		st_Curr = "ASC_IDLE"
				if values["_radio_manual_"]:	st_Curr = "MNL_IDLE"
			
			## ------------------------------------------------------------------------
			## Concerns camera-related inputs
			if st_Curr == "CAM_IDLE":
				st_Prev = st_Curr
				window["_btn_inputCam_"].update(disabled=False)
				window["frame_raw_0"].update(data=None)
				window["frame_raw_1"].update(data=None)
				window["frame_combined_0"].update(data=None)
				window["frame_combined_1"].update(data=None)
				if event in ("_btn_inputCam_"):
					st_Curr = "CAM_GET"
				if values["_radio_ascii_"] or values["_radio_manual_"]:
					st_Curr = "INIT"
			###	Given request, sets up camera to obtain images
			elif st_Curr == "CAM_GET": # State: Runs cameras & obtains pictures
				try:
					if (st_Curr != st_Prev): # Should come from "INIT"
						window["_btn_inputCam_"].update(disabled=False)
						#window["_btn_confirmCam_"].update(disabled=False)
						#window["_textRunCam_"].update("Press [CONFIRM] to confirm camera input")
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
					if event in ("_btn_inputCam_"):
						st_Curr = "CAM_SET"
					elif values["_radio_ascii_"] or values["_radio_manual_"]:
						getColor.cam_releaseCap(cap_0, cap_1)
						st_Curr = "INIT"
				except: # Given camera not connected or removed during run
					sg.PopupError(	"Unable to open/read camera.", 
									"Check that cameras are connected & able to be launched.", 
									title="Camera Error"	)
					st_Curr = "X"
			###	Given camera confirmation, obtains cubelets from such images
			elif st_Curr == "CAM_SET":
				window["_btn_inputCam_"].update(disabled=True)
				getColor.cam_releaseCap(cap_0, cap_1) # Releases OCV once done
				cubelets = initCam.cam_obtainCubelets(result_combined, result_color)
				getNew.printCube(cubelets)
				cube = getNew.obtainVirCube(50) # Debug purposes - generates new cube
				# Replace above line w/ verification of camera-obtained cubelet
				st_Curr = "MOVES_GET_CAM"
			###	Given cube parsed from images, evaluates moves from camera
			elif st_Curr == "MOVES_GET_CAM":
				ls_kocSolve, str_kocSolve = cubeSolve.solveCubeKoc(cubeSolve.parseCubeString(cube))
				ls_runMoves, str_runMoves = ls_kocSolve, str_kocSolve
				print(ls_runMoves)
				getNew.printCube(cube)
				st_Curr = "MOVES_SET"

			## ------------------------------------------------------------------------
			### Refers to ASCII-related inputs
			elif st_Curr == "ASC_IDLE":
				st_Prev = st_Curr
				window["frame_raw_0"].update(data=None)
				window["frame_raw_1"].update(data=None)
				window["frame_combined_0"].update(data=None)
				window["frame_combined_1"].update(data=None)
				#print("DEBUG: " + st_Curr + ", " + st_Prev)
				st_Curr = "ASC_GET"
			elif st_Curr == "ASC_GET":
				if (st_Curr != st_Prev):
					window["_btn_confirmFile_"].update(disabled=False)
					window["_btn_inputFile_"].update(disabled=False)
					window["_file_ascii_"].update(disabled=False)
					st_Prev = st_Curr
				if event in ("_btn_confirmFile_"):
					st_Curr = "ASC_SET"
				if values["_radio_cam_"] or values["_radio_manual_"]:
					st_Curr = "INIT"
			elif st_Curr == "ASC_SET":
				st_Prev = st_Curr
				window["_btn_confirmFile_"].update(disabled=True)
				window["_btn_inputFile_"].update(disabled=True)
				window["_file_ascii_"].update(disabled=True)
				try:
					fileMixup = open(str(values["_file_ascii_"]), 'r')
					str_Mixup = fileMixup.read()
					st_Curr = "MOVES_GET_ASC"
				except:
					sg.PopupError(	"Unable to read file.", 
									"Check that file is existent & legible.", 
									title="Invalid File")
					st_Curr = "X"
			elif st_Curr == "MOVES_GET_ASC":
				st_Prev = st_Curr
				str_ascii, bl_asciiValid = getAscii.returnParsedStr(str_Mixup) # Test list of moves
				if bl_asciiValid == True:
					ls_ascii = cubeSolve.getMovesList(str_ascii)
					ls_runMoves, str_runMoves = ls_ascii, str_ascii
					cube = getNew.obtainVirCube()
					st_Curr = "MOVES_SET"
				else:
					sg.PopupError(	"Invalid string.", 
									"Check that text in file conforms to input string format.", 
									title="Invalid File")
					st_Curr = "X"

				
			## ------------------------------------------------------------------------
			###	Given set of moves, prep program to run moves, including simulation
			elif st_Curr == "MOVES_SET":
				if (st_Curr != st_Prev): # Should come from "CAM_SET"
					window["_radio_ascii_"].update(disabled=True)
					window["_radio_cam_"].update(disabled=True)
					window["_radio_manual_"].update(disabled=True)
					drawCubelets(window, cube)
					window["_listMoves_"].update(disabled=False, values=str_runMoves)
					window["_slide_movesProgress_"].update(disabled=False, range=(0, len(str_runMoves)), value=0)
					window["_txt_moveCurrent_"].update("None")
					window["_txt_moveIndex_"].update(0)
					window["_btn_solve_"].update(disabled=False)
					st_Prev = st_Curr
				''' Given input into slider, simulates cube turning
				'''
				if event in ("_slide_movesProgress_"): # Displays cube changes throughout the solving algorithm
					# Given valid slider values & is changing position
					# Assumes cube is obtained & kociemba moves are valid
					# I.E.
					# If position is 0, show initial
					# If position is 1, show [0]
					# If position is 2, show [0] + [1]
					# ...
					cube_disp = deepcopy(cube)
					indexMove = int(values["_slide_movesProgress_"]) # Given float value of slider
					window["_txt_moveIndex_"].update(str(indexMove))
					window["_txt_moveCurrent_"].update("None")
					if (indexMove > 0): # Considers moves beyond default cube
						window["_txt_moveCurrent_"].update(str(str_runMoves[indexMove - 1]))
						for moveCurrent in range(indexMove):
							for i in range(ls_runMoves[moveCurrent][1]):
								cube_disp = scramble.moveFace(ls_runMoves[moveCurrent][0], cube_disp)
					drawCubelets(window, cube_disp)
				elif event in ("_btn_solve_"):
					# Once in this event, no termination permitted until solving is finished
					st_Curr = "MOVES_RUN"

			###	Given user confirmation to run moves, runs such moves
			elif st_Curr == "MOVES_RUN":
				window["_slide_movesProgress_"].update(disabled=True)
				window["_btn_solve_"].update(disabled=True)
				drawCubelets(window, cube)
				for index in range(len(ls_runMoves)):
					moveCurrent = ls_runMoves[index]
					window["_slide_movesProgress_"].update(value=(index + 1))
					window["_txt_moveIndex_"].update(str(index + 1))
					window["_txt_moveCurrent_"].update(str(str_runMoves[index]))
					#print(index + 1)
					# for i in range(moveCurrent[1]):
					# 	cube = scramble.moveFace(moveCurrent[0], cube)
					# 	# Audio - output per file
					# 	waveSine.audioInputSeq(moveCurrent[0])
					# Audio output of specific frequencies corresponding to face
					waveSine.audioInputSeq([moveCurrent])
					# Rotates & displays cube given mode
					for i in range(moveCurrent[1]): cube = scramble.moveFace(moveCurrent[0], cube)
					drawCubelets(window, cube)
					window.refresh()
				st_Curr = "DONE"

			### Given move completion, affirm with completion message
			elif st_Curr == "DONE":
				sg.Popup("Operation completed.", title="Completed")
				st_Curr = "INIT"
			
			## ------------------------------------------------------------------------
			# Given manual input mode selected
			elif st_Curr == "MNL_IDLE":
				window["_btn_man_U_"].update(disabled=False)
				window["_btn_man_R_"].update(disabled=False)
				window["_btn_man_F_"].update(disabled=False)
				window["_btn_man_D_"].update(disabled=False)
				window["_btn_man_L_"].update(disabled=False)
				window["_btn_man_B_"].update(disabled=False)
				window["_ls_mnl_mode_"].update(disabled=False)
				cube = getNew.obtainVirCube() # Generates default virtual cube to display movement
				drawCubelets(window, cube)
				st_Curr = "MNL_GET"
			elif st_Curr == "MNL_GET":
				st_Prev = st_Curr
				if values["_radio_cam_"] or values["_radio_ascii_"]:
					st_Curr = "INIT"
				if 	event in ([	"_btn_man_U_", "_btn_man_R_", "_btn_man_F_",\
								"_btn_man_D_", "_btn_man_L_", "_btn_man_B_"	]):
					move_mnl = event[len(event) - 2]
					st_Curr = "MNL_SET"

			elif st_Curr == "MNL_SET":
				print("Rotating face " + move_mnl)
				dict_ls_mnl = {	"Forward": 1, "Double": 2, "Reverse": 3	}
				mode_mnl = dict_ls_mnl[values["_ls_mnl_mode_"]]
				for i in range(mode_mnl):
					cube = scramble.moveFace(move_mnl, cube)
				waveSine.audioInputSeq([(move_mnl, mode_mnl)])
				drawCubelets(window, cube)
				window.refresh()
				st_Curr = "MNL_GET"
			
			## ------------------------------------------------------------------------
			else: # Given invalid state
				print("Invalid state!")
				st_Curr = "INIT"
		else: # Given invalid state
			print("Invalid state!")
			st_Curr = "INIT"
	window.close() # GUI loop exited - destroy window

# if __name__ == "__main__":
# 	main()