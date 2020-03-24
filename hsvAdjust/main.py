import PySimpleGUI as sg

# # Importing specific variables to be utilised in GUI
# from variables import dict_faceColor

# # Custom modules to obtain functions necessary
# import cubeGen_scramble as scramble
# import cubeGen_getNew as getNew
# import solve_cubeSolve as cubeSolve
# import solve_getAscii as getAscii
# import imgParse_getColor as getColor
# import imgParse_initCam as initCam
# import audio_waveSine as waveSine
import hsv_getColor as getColor
from var_def import default_hsv
#import hsv_initCam as initCam

def windowDefine():
	# Defines layout of HSV slider dialog boxes
	def tabHSV():
		slide_hsv_w = [	[	sg.Frame("Lower", [	[	sg.Text("H"), sg.Slider(key="_hsv_w_lo_h_", orientation="horizontal", range=(0, 179))	],
												[	sg.Text("S"), sg.Slider(key="_hsv_w_lo_s_", orientation="horizontal", range=(0, 255))	],
												[	sg.Text("V"), sg.Slider(key="_hsv_w_lo_v_", orientation="horizontal", range=(0, 255))	]
												])
							],
						[	sg.Frame("Upper", [	[	sg.Text("H"), sg.Slider(key="_hsv_w_up_h_", orientation="horizontal", range=(0, 179))	],
												[	sg.Text("S"), sg.Slider(key="_hsv_w_up_s_", orientation="horizontal", range=(0, 255))	],
												[	sg.Text("V"), sg.Slider(key="_hsv_w_up_v_", orientation="horizontal", range=(0, 255))	]
												])
							]
						]
		slide_hsv_r0 = [	[	sg.Frame("Lower", [	[	sg.Text("H"), sg.Slider(key="_hsv_r0_lo_h_", orientation="horizontal", range=(0, 179))	],
													[	sg.Text("S"), sg.Slider(key="_hsv_r0_lo_s_", orientation="horizontal", range=(0, 255))	],
													[	sg.Text("V"), sg.Slider(key="_hsv_r0_lo_v_", orientation="horizontal", range=(0, 255))	]
													])
								],
							[	sg.Frame("Upper", [	[	sg.Text("H"), sg.Slider(key="_hsv_r0_up_h_", orientation="horizontal", range=(0, 179))	],
													[	sg.Text("S"), sg.Slider(key="_hsv_r0_up_s_", orientation="horizontal", range=(0, 255))	],
													[	sg.Text("V"), sg.Slider(key="_hsv_r0_up_v_", orientation="horizontal", range=(0, 255))	]
													])
								]
						]
		slide_hsv_r1 = [	[	sg.Frame("Lower", [	[	sg.Text("H"), sg.Slider(key="_hsv_r1_lo_h_", orientation="horizontal", range=(0, 179))	],
													[	sg.Text("S"), sg.Slider(key="_hsv_r1_lo_s_", orientation="horizontal", range=(0, 255))	],
													[	sg.Text("V"), sg.Slider(key="_hsv_r1_lo_v_", orientation="horizontal", range=(0, 255))	]
													])
								],
							[	sg.Frame("Upper", [	[	sg.Text("H"), sg.Slider(key="_hsv_r1_up_h_", orientation="horizontal", range=(0, 179))	],
													[	sg.Text("S"), sg.Slider(key="_hsv_r1_up_s_", orientation="horizontal", range=(0, 255))	],
													[	sg.Text("V"), sg.Slider(key="_hsv_r1_up_v_", orientation="horizontal", range=(0, 255))	]
													])
								]
						]
		slide_hsv_o = [	[	sg.Frame("Lower", [	[	sg.Text("H"), sg.Slider(key="_hsv_o_lo_h_", orientation="horizontal", range=(0, 179))	],
												[	sg.Text("S"), sg.Slider(key="_hsv_o_lo_s_", orientation="horizontal", range=(0, 255))	],
												[	sg.Text("V"), sg.Slider(key="_hsv_o_lo_v_", orientation="horizontal", range=(0, 255))	]
												])
							],
						[	sg.Frame("Upper", [	[	sg.Text("H"), sg.Slider(key="_hsv_o_up_h_", orientation="horizontal", range=(0, 179))	],
												[	sg.Text("S"), sg.Slider(key="_hsv_o_up_s_", orientation="horizontal", range=(0, 255))	],
												[	sg.Text("V"), sg.Slider(key="_hsv_o_up_v_", orientation="horizontal", range=(0, 255))	]
												])
							]
						]
		slide_hsv_y = [	[	sg.Frame("Lower", [	[	sg.Text("H"), sg.Slider(key="_hsv_y_lo_h_", orientation="horizontal", range=(0, 179))	],
												[	sg.Text("S"), sg.Slider(key="_hsv_y_lo_s_", orientation="horizontal", range=(0, 255))	],
												[	sg.Text("V"), sg.Slider(key="_hsv_y_lo_v_", orientation="horizontal", range=(0, 255))	]
												])
							],
						[	sg.Frame("Upper", [	[	sg.Text("H"), sg.Slider(key="_hsv_y_up_h_", orientation="horizontal", range=(0, 179))	],
												[	sg.Text("S"), sg.Slider(key="_hsv_y_up_s_", orientation="horizontal", range=(0, 255))	],
												[	sg.Text("V"), sg.Slider(key="_hsv_y_up_v_", orientation="horizontal", range=(0, 255))	]
												])
							]
						]
		slide_hsv_g = [	[	sg.Frame("Lower", [	[	sg.Text("H"), sg.Slider(key="_hsv_g_lo_h_", orientation="horizontal", range=(0, 179))	],
												[	sg.Text("S"), sg.Slider(key="_hsv_g_lo_s_", orientation="horizontal", range=(0, 255))	],
												[	sg.Text("V"), sg.Slider(key="_hsv_g_lo_v_", orientation="horizontal", range=(0, 255))	]
												])
							],
						[	sg.Frame("Upper", [	[	sg.Text("H"), sg.Slider(key="_hsv_g_up_h_", orientation="horizontal", range=(0, 179))	],
												[	sg.Text("S"), sg.Slider(key="_hsv_g_up_s_", orientation="horizontal", range=(0, 255))	],
												[	sg.Text("V"), sg.Slider(key="_hsv_g_up_v_", orientation="horizontal", range=(0, 255))	]
												])
							]
						]
		slide_hsv_b = [	[	sg.Frame("Lower", [	[	sg.Text("H"), sg.Slider(key="_hsv_b_lo_h_", orientation="horizontal", range=(0, 179))	],
												[	sg.Text("S"), sg.Slider(key="_hsv_b_lo_s_", orientation="horizontal", range=(0, 255))	],
												[	sg.Text("V"), sg.Slider(key="_hsv_b_lo_v_", orientation="horizontal", range=(0, 255))	]
												])
							],
						[	sg.Frame("Upper", [	[	sg.Text("H"), sg.Slider(key="_hsv_b_up_h_", orientation="horizontal", range=(0, 179))	],
												[	sg.Text("S"), sg.Slider(key="_hsv_b_up_s_", orientation="horizontal", range=(0, 255))	],
												[	sg.Text("V"), sg.Slider(key="_hsv_b_up_v_", orientation="horizontal", range=(0, 255))	]
												])
							]
						]
		layout_hsv = [	[	sg.TabGroup([	[	sg.Tab("White", slide_hsv_w),
												sg.Tab("Red Lower", slide_hsv_r0),
												sg.Tab("Red Upper", slide_hsv_r1),
												sg.Tab("Orange", slide_hsv_o),
												sg.Tab("Yellow", slide_hsv_y),
												sg.Tab("Green", slide_hsv_g),
												sg.Tab("Blue", slide_hsv_b)
												]
											], tab_location="topleft")
							]
						]
		return layout_hsv
	sg.theme("Reddit") # Reddit theme applied (no orange, though - sad)
	layout_cam = [	[	sg.Button("Run/Stop", key="_btn_inputCam_"), sg.Button("Print HSV", key="_btn_printHsv_")
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
	layout_hsv = tabHSV()
	layout = [	[	sg.Frame("HSV Settings", layout_hsv),
					sg.Frame("Camera Layout", layout_cam)
					]
				]
	window = sg.Window("Window Title", layout, finalize=True, return_keyboard_events=True, use_default_focus=False)
	return window

def setHsvToSlider(window, vals_hsv):
	window["_hsv_w_lo_h_"].update(value=vals_hsv[0][0][0]	)
	window["_hsv_w_lo_s_"].update(value=vals_hsv[0][0][1]	)
	window["_hsv_w_lo_v_"].update(value=vals_hsv[0][0][2]	)
	window["_hsv_w_up_h_"].update(value=vals_hsv[0][1][0]	)
	window["_hsv_w_up_s_"].update(value=vals_hsv[0][1][1]	)
	window["_hsv_w_up_v_"].update(value=vals_hsv[0][1][2]	)
	
	window["_hsv_r0_lo_h_"].update(value=vals_hsv[1][0][0]	)
	window["_hsv_r0_lo_s_"].update(value=vals_hsv[1][0][1]	)
	window["_hsv_r0_lo_v_"].update(value=vals_hsv[1][0][2]	)
	window["_hsv_r0_up_h_"].update(value=vals_hsv[1][1][0]	)
	window["_hsv_r0_up_s_"].update(value=vals_hsv[1][1][1]	)
	window["_hsv_r0_up_v_"].update(value=vals_hsv[1][1][2]	)
	
	window["_hsv_r1_lo_h_"].update(value=vals_hsv[2][0][0]	)
	window["_hsv_r1_lo_s_"].update(value=vals_hsv[2][0][1]	)
	window["_hsv_r1_lo_v_"].update(value=vals_hsv[2][0][2]	)
	window["_hsv_r1_up_h_"].update(value=vals_hsv[2][1][0]	)
	window["_hsv_r1_up_s_"].update(value=vals_hsv[2][1][1]	)
	window["_hsv_r1_up_v_"].update(value=vals_hsv[2][1][2]	)
	
	window["_hsv_o_lo_h_"].update(value=vals_hsv[3][0][0]	)
	window["_hsv_o_lo_s_"].update(value=vals_hsv[3][0][1]	)
	window["_hsv_o_lo_v_"].update(value=vals_hsv[3][0][2]	)
	window["_hsv_o_up_h_"].update(value=vals_hsv[3][1][0]	)
	window["_hsv_o_up_s_"].update(value=vals_hsv[3][1][1]	)
	window["_hsv_o_up_v_"].update(value=vals_hsv[3][1][2]	)
	
	window["_hsv_y_lo_h_"].update(value=vals_hsv[4][0][0]	)
	window["_hsv_y_lo_s_"].update(value=vals_hsv[4][0][1]	)
	window["_hsv_y_lo_v_"].update(value=vals_hsv[4][0][2]	)
	window["_hsv_y_up_h_"].update(value=vals_hsv[4][1][0]	)
	window["_hsv_y_up_s_"].update(value=vals_hsv[4][1][1]	)
	window["_hsv_y_up_v_"].update(value=vals_hsv[4][1][2]	)
	
	window["_hsv_g_lo_h_"].update(value=vals_hsv[5][0][0]	)
	window["_hsv_g_lo_s_"].update(value=vals_hsv[5][0][1]	)
	window["_hsv_g_lo_v_"].update(value=vals_hsv[5][0][2]	)
	window["_hsv_g_up_h_"].update(value=vals_hsv[5][1][0]	)
	window["_hsv_g_up_s_"].update(value=vals_hsv[5][1][1]	)
	window["_hsv_g_up_v_"].update(value=vals_hsv[5][1][2]	)
	
	window["_hsv_b_lo_h_"].update(value=vals_hsv[6][0][0]	)
	window["_hsv_b_lo_s_"].update(value=vals_hsv[6][0][1]	)
	window["_hsv_b_lo_v_"].update(value=vals_hsv[6][0][2]	)
	window["_hsv_b_up_h_"].update(value=vals_hsv[6][1][0]	)
	window["_hsv_b_up_s_"].update(value=vals_hsv[6][1][1]	)
	window["_hsv_b_up_v_"].update(value=vals_hsv[6][1][2]	)
	return window

def getHsvFromSlider(window):
	hsv_w_lo = [values["_hsv_w_lo_h_"], values["_hsv_w_lo_s_"], values["_hsv_w_lo_v_"]]
	hsv_w_up = [values["_hsv_w_up_h_"], values["_hsv_w_up_s_"], values["_hsv_w_up_v_"]]
	hsv_w = [hsv_w_lo, hsv_w_up]
	hsv_r0_lo = [values["_hsv_r0_lo_h_"], values["_hsv_r0_lo_s_"], values["_hsv_r0_lo_v_"]]
	hsv_r0_up = [values["_hsv_r0_up_h_"], values["_hsv_r0_up_s_"], values["_hsv_r0_up_v_"]]
	hsv_r0 = [hsv_r0_lo, hsv_r0_up]
	hsv_r1_lo = [values["_hsv_r1_lo_h_"], values["_hsv_r1_lo_s_"], values["_hsv_r1_lo_v_"]]
	hsv_r1_up = [values["_hsv_r1_up_h_"], values["_hsv_r1_up_s_"], values["_hsv_r1_up_v_"]]
	hsv_r1 = [hsv_r1_lo, hsv_r1_up]
	hsv_o_lo = [values["_hsv_o_lo_h_"], values["_hsv_o_lo_s_"], values["_hsv_o_lo_v_"]]
	hsv_o_up = [values["_hsv_o_up_h_"], values["_hsv_o_up_s_"], values["_hsv_o_up_v_"]]
	hsv_o = [hsv_o_lo, hsv_o_up]
	hsv_y_lo = [values["_hsv_y_lo_h_"], values["_hsv_y_lo_s_"], values["_hsv_y_lo_v_"]]
	hsv_y_up = [values["_hsv_y_up_h_"], values["_hsv_y_up_s_"], values["_hsv_y_up_v_"]]
	hsv_y = [hsv_y_lo, hsv_y_up]
	hsv_g_lo = [values["_hsv_g_lo_h_"], values["_hsv_g_lo_s_"], values["_hsv_g_lo_v_"]]
	hsv_g_up = [values["_hsv_g_up_h_"], values["_hsv_g_up_s_"], values["_hsv_g_up_v_"]]
	hsv_g = [hsv_g_lo, hsv_g_up]
	hsv_b_lo = [values["_hsv_b_lo_h_"], values["_hsv_b_lo_s_"], values["_hsv_b_lo_v_"]]
	hsv_b_up = [values["_hsv_b_up_h_"], values["_hsv_b_up_s_"], values["_hsv_b_up_v_"]]
	hsv_b = [hsv_b_lo, hsv_b_up]
	hsv_list = [hsv_w, hsv_r0, hsv_r1, hsv_o, hsv_y, hsv_g, hsv_b]
	return hsv_list


if __name__ == "__main__":
	# Defines state machine verification
	ls_state = [	"INIT", 
					"CAM_IDLE", "CAM_GET",
					"DONE"
					]
	st_Prev, st_Curr = "DONE", "INIT" # Defines startup states

	vals_hsv = default_hsv
	window = setHsvToSlider(windowDefine(), vals_hsv)
	while True: 
		# Reads events & values in window, provided certain small update & delay
		event, values = window.read(timeout=0, timeout_key='timeout')
		if (st_Curr != st_Prev): print("States: " + st_Curr + ", " + st_Prev)

		if event in (None, "Exit"): # Given cancel clicked, exits program
			break
		if event in ("_btn_printHsv_"):
			print(vals_hsv)
		if (st_Prev in ls_state) and (st_Curr in ls_state):
			if st_Curr == "INIT": # State: Idle-waiting to initialise camera
				st_Prev = st_Curr
				window["frame_raw_0"].update(filename='', size=(200, 200))
				window["frame_raw_1"].update(filename='', size=(200, 200))
				window["frame_combined_0"].update(filename='', size=(200, 200))
				window["frame_combined_1"].update(filename='', size=(200, 200))
				st_Curr = "CAM_IDLE"
			elif st_Curr == "CAM_IDLE":
				st_Prev = st_Curr
				if event in ("_btn_inputCam_"):
					st_Curr = "CAM_GET"
			elif st_Curr == "CAM_GET": # State: Runs cameras & obtains pictures
				try:
					if (st_Curr != st_Prev):
						cap_0, cap_1 = getColor.cam_initCap()
						st_Prev = st_Curr
					vals_hsv = getHsvFromSlider(window)
					result_raw, result_combined, result_color = getColor.cam_obtain(cap_0, cap_1, vals_hsv)
					imgbytes_raw = (	getColor.cam_getImgbytes(result_raw[0], 200	),
										getColor.cam_getImgbytes(result_raw[1], 200	)	)
					imgbytes_combined = (	getColor.cam_getImgbytes(result_combined[0], 200	),
											getColor.cam_getImgbytes(result_combined[1], 200	)	)
					window["frame_raw_0"].update(data=imgbytes_raw[0])
					window["frame_raw_1"].update(data=imgbytes_raw[1])
					window["frame_combined_0"].update(data=imgbytes_combined[0])
					window["frame_combined_1"].update(data=imgbytes_combined[1])
					if event in ("_btn_inputCam_"):
						getColor.cam_releaseCap(cap_0, cap_1)
						st_Curr = "INIT"
				except: # Given camera not connected or removed during run
					sg.PopupError(	"Unable to open/read camera.", 
									"Check that cameras are connected & able to be launched.", 
									title="Camera Error"	)
					st_Curr = "INIT"
	window.close() # GUI loop exited - destroy window