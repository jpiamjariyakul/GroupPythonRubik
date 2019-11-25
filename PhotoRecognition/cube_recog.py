### Imports prerequisites & libraries
import cv2
import numpy as np
#from matplotlib import pyplot as plt
#from datetime import datetime



### Declares faces visible to camera & to be analysed
# Coord system per following
'''
[0,0][0,1][0,2]
[1,0][1,1][1,2]
[2,0][2,1][2,2]
'''
# Tuple storing pixels to check in image
'''
coord = (
			(	# Pixels on face UP
                (	( 96,	 96),	(123,	 86),	(148,	 76)	),
                (   (122,	107),	(150,	 96),	(175,	 85)	),
                (	(153,	120),	(181,	107),	(204,	 94)	)
            ),
			(	# Pixels on face LEFT
                (   ( 80,	115),	(107,	128),	(137,	141)	),
                (   ( 87,	137),	(110,	149),	(136,	163)	),
                (   ( 91,	155),	(112,	168),	(135,	181)	)
            ),
			(	# Pixels on face FRONT
                (	(169,	141),	(196,	128),	(218,	115)	),
                (   (165,	163),	(190,	149),	(213,	137)	),
                (   (163,	181),	(187,	168),	(209,	155)	)
            )
		)
'''

# Tuple storing pixels to check in image - amended later to accommodate rig
# NB: OpenCV uses a (Y,X) coordinate system
coord_yx = (
			(	# Pixels on face UP
                (	( 96,	 96),	( 86, 	123),	(76, 	148)	),
                (   (107,	122),	( 96,	150),	(85,	175)	),
                (	(120,	153),	(107,	181),	(94,	204)	)
            ),
			(	# Pixels on face LEFT
                (   ( 115,	80),	(128,	107),	(141,	137)	),
                (   ( 137,	87),	(149,	110),	(163,	136)	),
                (   ( 155,	91),	(168,	112),	(181,	135)	)
            ),
			(	# Pixels on face FRONT
                (	(141,	169),	(128,	196),	(115,	218)	),
                (   (163,	165),	(149,	190),	(137,	213)	),
                (   (181,	163),	(168,	187),	(155,	209)	)
            )
		)

def nothing(x):
    pass

# Defines color at coordinates given
def checkColor(	hsv_combined,
				hsv_white, hsv_red, hsv_orange,
				hsv_yellow, hsv_green, hsv_blue):
	# Only uses array values & not the images themselves
	if np.any(hsv_combined == hsv_blue): return "B"
	elif np.any(hsv_combined == hsv_white): return "W"
	elif np.any(hsv_combined == hsv_red): return "R"
	elif np.any(hsv_combined == hsv_orange): return "O"
	elif np.any(hsv_combined == hsv_yellow): return "Y"
	elif np.any(hsv_combined == hsv_green): return "G"

# Verifies color at pixel & its surroundings whether it's black or otherwise
def verifyColor(	face, row, column, c_combined,
					c_white, c_red, c_orange,
					c_yellow, c_green, c_blue):
	coord_row, coord_col = coord_yx[face][row][column][0], coord_yx[face][row][column][1]
	print("XY [" + str(face) + " " + str(row) + " " + str(column) + "]: (" + str(coord_row) + ", " + str(coord_col) + ")")
	print("Found on first attempt: " + str(np.any(c_combined[coord_row][coord_col] != 0)))
	# Check if at specified coords there are colors
	if np.any(c_combined[coord_row][coord_col] != 0):
		# Passes HSV values instead of the images
		color = checkColor(	c_combined[coord_row][coord_col],	\
							c_white[coord_row][coord_col], 		\
							c_red[coord_row][coord_col], 		\
							c_orange[coord_row][coord_col], 	\
							c_yellow[coord_row][coord_col], 	\
							c_green[coord_row][coord_col], 		\
							c_blue[coord_row][coord_col])
		print("Color at (" + str(coord_row) + ", " + str(coord_col) + "): " + str(color))
		print("------------------------")
	else: # Otherwise, iterate through 2 layers	until color found, or error
		layerMax = 3 # Max number of iterational layers to expand from original point
		i = j = -1 * layerMax
		i_initial = i
		while (True):
			if np.any(c_combined[coord_row + j][coord_col + i] != 0) and (i != 0) and (j != 0):
				color = checkColor(	c_combined[coord_row + j][coord_col + i],	\
									c_white[coord_row + j][coord_col + i], 		\
									c_red[coord_row + j][coord_col + i], 		\
									c_orange[coord_row + j][coord_col + i], 	\
									c_yellow[coord_row + j][coord_col + i], 	\
									c_green[coord_row + j][coord_col + i], 		\
									c_blue[coord_row + j][coord_col + i])
				print("Color at (" + str(coord_row + j) + ", " + str(coord_col + i) + "): " + str(color))
				print("------------------------")
				break
			else:
				print("!!! - Invalid color at " + str(coord_row + j) + ", " + str(coord_col + i) + " - adding range")
				if i >= layerMax:
					i = i_initial
					j += 1
				else: i += 1
				if j >= layerMax:
					color = "U"
					print("ERROR - color undefined")
					print("------------------------")
					break
	return color


# Creates a resizable window frame - one loads video/image into it
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
# Program functions perfectly normal w/out line in

def main():
	"""Stage 1.1: Obtain masks for each individual color in image"""
	# Captures frame-by-frame
	frame = cv2.imread("image_02.jpg", cv2.IMREAD_COLOR)

	# Gaussian filter is applied to captured image - remove noises
	image_gaussian = cv2.GaussianBlur(frame, (5, 5), 0)

	# Converts color-space from BGR to HSV
	frame_hsv = cv2.cvtColor(image_gaussian, cv2.COLOR_BGR2HSV)

	# In OpenCV, range is [179, 255, 255]
	# Defines boundaries in HSV for the color white
	white_lower = np.array([0, 0, 200])
	white_upper = np.array([179, 20, 255])
	# Defines boundaries in HSV for the color red
	red_lower = np.array([0, 132, 35])
	red_upper = np.array([12, 255, 255])
	# Defines boundaries in HSV for the color orange
	orange_lower = np.array([13, 77, 208])
	orange_upper = np.array([24, 255, 255])
	# Defines boundaries in HSV for the color yellow
	yellow_lower = np.array([25, 60, 141])
	yellow_upper = np.array([65, 255, 255])
	# Defines boundaries in HSV for the color green
	green_lower = np.array([45, 53, 88])
	green_upper = np.array([91, 255, 255])
	# Defines boundaries in HSV for the color blue
	blue_lower = np.array([101, 128, 128])
	blue_upper = np.array([150, 255, 255])

	# Sets threshold to the HSV image
	mask_white	= cv2.inRange(frame_hsv, white_lower, 	white_upper) # Obtains white
	mask_red 	= cv2.inRange(frame_hsv, red_lower, 	red_upper) # Obtains red
	mask_orange	= cv2.inRange(frame_hsv, orange_lower, 	orange_upper) # Obtains orange
	mask_yellow	= cv2.inRange(frame_hsv, yellow_lower, 	yellow_upper) # Obtains yellow
	mask_green 	= cv2.inRange(frame_hsv, green_lower, 	green_upper) # Obtains green
	mask_blue 	= cv2.inRange(frame_hsv, blue_lower, 	blue_upper) # Obtains blue
	# Combines previous HSV masks together
	mask_combined = mask_yellow + mask_red + mask_orange + mask_green + mask_blue + mask_white

	# Sets erosion filter factor
	kernel = np.ones((5, 5), np.uint8)
	# Eroding reduces noise in image
	mask_combined = cv2.erode(mask_combined,  kernel)

	# Finds contours of image
	#contours, _ = cv2.findContours(mask_combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	# Applies a bitwise-AND operation on the combined mask and original (blurred) image
	result_final = cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_combined)
	# Resize image to normalised size, i.e. 300x300
	result_final = cv2.resize(result_final, (300, 300))
	# This allows for a normalised coordinate system afterwards
	# Such will be used during detecting each facelets, per each point in image

	# Resizes previous individual masks to allow color checking
	result_white = 	cv2.resize(
						cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_white),
						(300, 300)
					)
	result_red = 	cv2.resize(
						cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_red),
						(300, 300)
					)
	result_orange = cv2.resize(
						cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_orange),
						(300, 300)
					)
	result_yellow = cv2.resize(
						cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_yellow),
						(300, 300)
					)
	result_green = 	cv2.resize(
						cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_green),
						(300, 300)
					)
	result_blue = 	cv2.resize(
						cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_blue),
						(300, 300)
					)
	result_combined = result_white + result_red + result_orange + result_yellow + result_green + result_blue


	"""Stage 1.2: Obtain & validate pixel colors in each cubelet"""
	# Defines individual faces & cubelets
	cubelets = []
	# Loop to fill all rows/columns
	for face in range(3):
		cubelets.append([]) # Creates superlist for faces
		for row in range(3):
			cubelets[face].append([]) # Creates sublist for rows
			for column in range(3):
				cubelets[face][row].append(verifyColor(	face, row, column, result_final,
														result_white, result_red, result_orange,
														result_yellow, result_green, result_blue
														))
	print(str(cubelets[0][0]) + " | " + str(cubelets[1][0]) + " | " + str(cubelets[2][0]))
	print(str(cubelets[0][1]) + " | " + str(cubelets[1][1]) + " | " + str(cubelets[2][1]))
	print(str(cubelets[0][2]) + " | " + str(cubelets[1][2]) + " | " + str(cubelets[2][2]))

	while(True):
		'''
		# Forms contours around lines
		for count in contours:
			# Question: what does this line do?
			approx = cv2.approxPolyDP(count, 0.1 * cv2.arcLength(count, True), True)
			area = cv2.contourArea(count)
			# Area factor of 500 selected - 
			if area > 500:
				cv2.drawContours(image_gaussian, [count], 0, (0, 255, 0), 2)
		'''
		# Displays image/video in frame
		cv2.imshow("Frame", result_final)
		# Recognises keystroke
		keystroke = cv2.waitKey(0) & 0xFF
		#if keystroke == 27: # wait for ESC key to exit
		if keystroke == ord('s'): # wait for 's' key to save image
			cv2.imwrite("image_resized.jpg", result_final)
			print("File written")
			break
		else:
			break
	# With everything done, release capture
	cv2.destroyAllWindows()

main()