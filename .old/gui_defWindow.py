import PySimpleGUI as sg

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

def initWindow(window):
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