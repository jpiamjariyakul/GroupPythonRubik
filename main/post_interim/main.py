### Imports prerequisites & libraries
import cv2
import numpy as np
import color
#import audio
import solving

'''
Order of Kociemba algorithm input is in following order: URFDLB
'''

# Creates a resizable window frame - one loads video/image into it
#cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
# Program functions perfectly normal w/out line in

def colorFrames(frame):
	# Gaussian filter is applied to captured image - remove noises
	image_gaussian = cv2.GaussianBlur(frame, (5, 5), 0)
	frame_hsv = cv2.cvtColor(image_gaussian, cv2.COLOR_BGR2HSV)	# Converts color-space from BGR to HSV

	#white_lower = np.array([100, 53, 0])
	#white_upper = np.array([120, 178, 255])

	# In OpenCV, range is [179, 255, 255]
	# Defines boundaries in HSV for different colors (in order WROYGB)
	# IE hsv_colorRange[2][0] = (np.array([13, 77, 208]) - such is lower-bound of red HSV values
	hsv_colorRange = (	(np.array([0, 0, 200]),		np.array([179, 20, 255])),
						(np.array([0, 132, 35]),	np.array([12, 255, 255])),
						(np.array([13, 77, 208]), 	np.array([24, 255, 255])),
						(np.array([25, 60, 141]), 	np.array([65, 255, 255])),
						(np.array([45, 53, 88]), 	np.array([91, 255, 255])),
						(np.array([101, 128, 128]), np.array([150, 255, 255]))
				)

	# Sets threshold to the HSV image - iterates over all six colors
	mask_color = []
	[mask_color.append(cv2.inRange(frame_hsv,	hsv_colorRange[i][0],	hsv_colorRange[i][1])) for i in range(6)]

	# Combines previous HSV masks together
	kernel = np.ones((5, 5), np.uint8)	# Sets erosion filter factor
	mask_combined = cv2.erode((mask_color[0] + mask_color[1] + mask_color[2] + mask_color[3] + mask_color[4] + mask_color[5]), kernel)
	# Eroding reduces noise in image

	# Resizes raw image from gaussian image
	result_raw = cv2.resize(image_gaussian, (300, 300))
	# Resizes previous individual masks to allow color checking
	# Simultaneously applies a bitwise-AND operation on the combined mask and original (blurred) image
	# This allows for a normalised coordinate system afterwards
	# Such will be used during detecting each facelets, per each point in image
	result_color = []
	[result_color.append(cv2.resize(cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_color[i]), (300, 300))) for i in range(6)]
	result_combined = result_color[0] + result_color[1] + result_color[2] + result_color[3] + result_color[4] + result_color[5]
	return result_raw, result_combined, result_color

def main():
	"""Stage 1.1: Obtain masks for each individual color in image"""
	#frame = cv2.imread("image_prescaled.jpg", cv2.IMREAD_COLOR)	# Debug purposes only
	cap = cv2.VideoCapture(0)
	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()
		frame = cv2.resize(frame, (300, 300))
		result_raw, result_combined, result_color = colorFrames(frame)

		red_pixel = (0, 0, 255)
		dot_radius = 3
		for face in range(len(color.coord_yx)):
			for row in range(len(color.coord_yx[face])):
				for column in range(len(color.coord_yx[face][row])):
					coord_xy = (color.coord_yx[face][row][column][1], color.coord_yx[face][row][column][0])
					img = cv2.circle(result_raw, coord_xy, dot_radius, (red_pixel), -1)

		cv2.imshow("Raw", result_raw)	# Displays image/video in frame
		cv2.imshow("Combined", result_combined)
		cv2.imshow("White", result_color[0])
		cv2.imshow("Red", result_color[1])
		cv2.imshow("Orange", result_color[2])
		cv2.imshow("Yellow", result_color[3])
		cv2.imshow("Green", result_color[4])
		cv2.imshow("Blue", result_color[5])

		keystroke = cv2.waitKey(1) & 0xFF	# Recognises keystroke
		if keystroke == 32: # wait for spacebar to run recognition
			cap.release()
			"""Stage 1.2: Obtain & validate pixel colors in each cubelet"""
			cubelets = []	# Defines individual faces & cubelets
			for face in range(3):
				cubelets.append([]) # Creates sublist for face
				for row in range(3):	# Loop to fill all rows/columns
					cubelets[face].append([]) # Creates sublist for rows
					for column in range(3):
						cubelets[face][row].append(color.verifyColor(	face, row, column, result_combined,
																		result_color[0], result_color[1], result_color[2],
																		result_color[3], result_color[4], result_color[5]
																		))
			#cv2.imwrite("image_resized.jpg", result_raw)
			print(str(cubelets[0][0]) + " | " + str(cubelets[1][0]) + " | " + str(cubelets[2][0]))
			print(str(cubelets[0][1]) + " | " + str(cubelets[1][1]) + " | " + str(cubelets[2][1]))
			print(str(cubelets[0][2]) + " | " + str(cubelets[1][2]) + " | " + str(cubelets[2][2]))

			#n = solving.algorithmSolve(cubelets)
			n = 0
			#print("File written")
			break
	print("Turns required: " + str(n))
	#audio.outputAudioTurns(n)
	print("Outputting signal for " + str(n) + " seconds")
	cv2.destroyAllWindows()	# With everything done, release capture
	print("Done!")
main()