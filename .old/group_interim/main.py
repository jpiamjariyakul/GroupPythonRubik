### Imports prerequisites & libraries
import cv2
import numpy as np
import color
import audio
import solving
import string
import kociemba

# Creates a resizable window frame - one loads video/image into it
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
# Program functions perfectly normal w/out line in

def main():
	"""Stage 1.1: Obtain masks for each individual color in image"""
	#frame = cv2.imread("image_02.jpg", cv2.IMREAD_COLOR)	# Captures frame-by-frame
	cap = cv2.VideoCapture(1)
	cap1 = cv2.VideoCapture(2)
	image_no = 0
	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()
		ret, frame1 = cap1.read()
		frame = cv2.resize(frame, (300, 300))
		#frame1 = cv2.resize(frame1, (300, 300))

		# Gaussian filter is applied to captured image - remove noises
		image_gaussian = cv2.GaussianBlur(frame, (5, 5), 0)
		frame_hsv = cv2.cvtColor(image_gaussian, cv2.COLOR_BGR2HSV)# Converts color-space from BGR to HSV
		image_gaussian1 = cv2.GaussianBlur(frame1, (5, 5), 0)
		frame1_hsv = cv2.cvtColor(image_gaussian1, cv2.COLOR_BGR2HSV)

		# In OpenCV, range is [179, 255, 255]
		# Defines boundaries in HSV for the color white
		#hsv_white = [np.array([0, 0, 200]), np.array([179, 20, 255])]
		white_lower = np.array([0, 0, 176])
		white_upper = np.array([34, 115, 255])
		#white_lower = np.array([100, 53, 0])
		#white_upper = np.array([123, 176, 250])
		# Defines boundaries in HSV for the color red
		red_lower = np.array([0, 51, 53])
		red_upper = np.array([12, 255, 180])
		red_lower1 = np.array([170, 50, 50])
		red_upper1 = np.array([180, 255, 255])
		# Defines boundaries in HSV for the color orange
		orange_lower = np.array([0, 173, 200])
		orange_upper = np.array([31, 237, 255])

		# Defines boundaries in HSV for the color yellow
		yellow_lower = np.array([16, 132, 194])
		yellow_upper = np.array([100, 160, 255])
		# Defines boundaries in HSV for the color green
		green_lower = np.array([45, 53, 88])
		green_upper = np.array([91, 255, 255])
		# Defines boundaries in HSV for the color blue
		blue_lower = np.array([101, 128, 128])
		blue_upper = np.array([150, 255, 255])

		# Sets threshold to the HSV image
		mask_white	= cv2.inRange(frame_hsv, white_lower, 	white_upper) # Obtains white
		mask_red1 = cv2.inRange(frame_hsv, red_lower, red_upper)  # Obtains red
		mask_red2 = cv2.inRange(frame_hsv, red_lower1, red_upper1)
		mask_red = mask_red1 + mask_red2 # Obtains red
		mask_orange	= cv2.inRange(frame_hsv, orange_lower, 	orange_upper) # Obtains orange
		mask_yellow	= cv2.inRange(frame_hsv, yellow_lower, 	yellow_upper) # Obtains yellow
		mask_green 	= cv2.inRange(frame_hsv, green_lower, 	green_upper) # Obtains green
		mask_blue 	= cv2.inRange(frame_hsv, blue_lower, 	blue_upper) # Obtains blue
		# Second set of mask for second camera
		mask_white_1	= cv2.inRange(frame1_hsv, white_lower, 	white_upper) # Obtains white
		mask_red1_1 = cv2.inRange(frame1_hsv, red_lower, red_upper)  # Obtains red
		mask_red2_1 = cv2.inRange(frame1_hsv, red_lower1, red_upper1)
		mask_red_1 = mask_red1_1 + mask_red2_1 # Obtains red
		mask_orange_1	= cv2.inRange(frame1_hsv, orange_lower, 	orange_upper) # Obtains orange
		mask_yellow_1	= cv2.inRange(frame1_hsv, yellow_lower, 	yellow_upper) # Obtains yellow
		mask_green_1 	= cv2.inRange(frame1_hsv, green_lower, 	green_upper) # Obtains green
		mask_blue_1 	= cv2.inRange(frame1_hsv, blue_lower, 	blue_upper) # Obtains blue
		# Combines previous HSV masks together
		mask_combined = mask_yellow + mask_red + mask_orange + mask_green + mask_blue + mask_white
		mask_combined_1 = mask_yellow_1 + mask_red_1 + mask_orange_1 + mask_green_1 + mask_blue_1 + mask_white_1

		kernel = np.ones((5, 5), np.uint8)	# Sets erosion filter factor
		mask_combined = cv2.erode(mask_combined,  kernel)	# Eroding reduces noise in image
		mask_combined_1 = cv2.erode(mask_combined_1, kernel)
		# Applies a bitwise-AND operation on the combined mask and original (blurred) image
		result_final = cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_combined)
		result_final_1 = cv2.bitwise_and(image_gaussian1, image_gaussian1, mask=mask_combined_1)
		result_final = cv2.resize(result_final, (300, 300)) # Resize image to normalised size, i.e. 300x300
		result_final_1 = cv2.resize(result_final_1, (300, 300))
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

		#Second set of results
		result_white_1 = 	cv2.resize(
							cv2.bitwise_and(image_gaussian1, image_gaussian1, mask=mask_white_1),
							(300, 300)
						)
		result_red_1 = 	cv2.resize(
							cv2.bitwise_and(image_gaussian1, image_gaussian1, mask=mask_red_1),
							(300, 300)
						)
		result_orange_1 = cv2.resize(
							cv2.bitwise_and(image_gaussian1, image_gaussian1, mask=mask_orange_1),
							(300, 300)
						)
		result_yellow_1 = cv2.resize(
							cv2.bitwise_and(image_gaussian1, image_gaussian1, mask=mask_yellow_1),
							(300, 300)
						)
		result_green_1 = 	cv2.resize(
							cv2.bitwise_and(image_gaussian1, image_gaussian1, mask=mask_green_1),
							(300, 300)
						)
		result_blue_1 = 	cv2.resize(
							cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_blue_1),
							(300, 300)
						)
		result_combined_1 = result_white_1 + result_red_1 + result_orange_1 + result_yellow_1 + result_green_1 + result_blue_1

		red_pixel = (0, 0, 255)
		img = cv2.circle(frame, (100, 100), 6, (red_pixel), -1)
		img = cv2.circle(frame, (150, 100), 6, (red_pixel), -1)
		img = cv2.circle(frame, (200, 100), 6, (red_pixel), -1)
		img = cv2.circle(frame, (100, 150), 6, (red_pixel), -1)
		img = cv2.circle(frame, (150, 150), 6, (red_pixel), -1)
		img = cv2.circle(frame, (200, 150), 6, (red_pixel), -1)
		img = cv2.circle(frame, (100, 200), 6, (red_pixel), -1)
		img = cv2.circle(frame, (150, 200), 6, (red_pixel), -1)
		img = cv2.circle(frame, (200, 200), 6, (red_pixel), -1)

		cv2.imshow("Frame", frame)	# Displays image/video in frame
		cv2.imshow("Frame1", frame1)
		# cv2.imshow("Combined", result_combined)
		# cv2.imshow("White", result_white)
		# cv2.imshow("Red", result_red)
		# cv2.imshow("Orange", result_orange)
		# cv2.imshow("Yellow", result_yellow)
		# cv2.imshow("Green", result_green)
		# cv2.imshow("Blue", result_blue)

		keystroke = cv2.waitKey(1) & 0xFF	# Recognises keystroke
		if keystroke == 27:  # wait for ESC key to exit
			break
		if keystroke == ord('r'): # wait for 's' key to save image
			image_no = 0
			print("image counter resetted")
		if keystroke == ord('s'): # wait for 's' key to save image
		#if keystroke == 32:
			#cap.release()
			if image_no == 0:
				image_no += 1
				"""Stage 1.2: Obtain & validate pixel colors in each cubelet"""
				cubelets = []	# Defines individual faces & cubelets
				for row in range(3):	# Loop to fill all rows/columns
					cubelets.append([]) # Creates sublist for rows
					for column in range(3):
						cubelets[row].append(color.verifyColor(	row, column, result_combined,
															result_white, result_red, result_orange,
															result_yellow, result_green, result_blue
															))
				cv2.imwrite("image_resized.jpg", result_final)
				cubelets_list = cubelets
				print(str(cubelets_list))
				cubelets = []
				for row in range(3):	# Loop to fill all rows/columns
					cubelets.append([]) # Creates sublist for rows
					for column in range(3):
						cubelets[row].append(color.verifyColor(	row, column, result_combined_1,
															result_white_1, result_red_1, result_orange_1,
															result_yellow_1, result_green_1, result_blue_1
															))

				cv2.imwrite("image_resized_1.jpg", result_final_1)
				print(str(cubelets[0]))
				print(str(cubelets[1]))
				print(str(cubelets[2]))
				cubelets_list.append(cubelets)
				print(cubelets_list)
				print (image_no)
			elif image_no == 1:
				image_no += 1
				cubelets = []  # Defines individual faces & cubelets
				for row in range(3):  # Loop to fill all rows/columns
					cubelets.append([])  # Creates sublist for rows
					for column in range(3):
						cubelets[row].append(color.verifyColor(row, column, result_combined,
															   result_white, result_red, result_orange,
															   result_yellow, result_green, result_blue
															   ))
				cv2.imwrite("image_resized.jpg", result_final)
				print(str(cubelets[0]))
				print(str(cubelets[1]))
				print(str(cubelets[2]))
				cubelets_list.append(cubelets)
				print (cubelets_list)
				print (image_no)
			elif image_no == 2:
				image_no += 1
				cubelets = []  # Defines individual faces & cubelets
				for row in range(3):  # Loop to fill all rows/columns
					cubelets.append([])  # Creates sublist for rows
					for column in range(3):
						cubelets[row].append(color.verifyColor(row, column, result_combined,
															   result_white, result_red, result_orange,
															   result_yellow, result_green, result_blue
															   ))
				cv2.imwrite("image_resized.jpg", result_final)
				print(str(cubelets[0]))
				print(str(cubelets[1]))
				print(str(cubelets[2]))
				cubelets_list.append(cubelets)
				print (cubelets_list)
				print (image_no)

			elif image_no == 3:
				image_no += 1
				cubelets = []  # Defines individual faces & cubelets
				for row in range(3):  # Loop to fill all rows/columns
					cubelets.append([])  # Creates sublist for rows
					for column in range(3):
						cubelets[row].append(color.verifyColor(row, column, result_combined,
															   result_white, result_red, result_orange,
															   result_yellow, result_green, result_blue
															   ))
				cv2.imwrite("image_resized.jpg", result_final)
				print(str(cubelets[0]))
				print(str(cubelets[1]))
				print(str(cubelets[2]))
				cubelets_list.append(cubelets)
				for_kociemba = str(cubelets_list)
				print (for_kociemba)
				print (image_no)
			elif image_no == 4:
				image_no += 1
				cubelets = []  # Defines individual faces & cubelets
				for row in range(3):  # Loop to fill all rows/columns
					cubelets.append([])  # Creates sublist for rows
					for column in range(3):
						cubelets[row].append(color.verifyColor(row, column, result_combined,
															   result_white, result_red, result_orange,
															   result_yellow, result_green, result_blue
															   ))
				cv2.imwrite("image_resized.jpg", result_final)
				print(str(cubelets[0]))
				print(str(cubelets[1]))
				print(str(cubelets[2]))
				cubelets_list.append(cubelets)
				print (for_kociemba)
				print (image_no)

			elif image_no == 5:
				image_no += 1
				cubelets = []  # Defines individual faces & cubelets
				for row in range(3):  # Loop to fill all rows/columns
					cubelets.append([])  # Creates sublist for rows
					for column in range(3):
						cubelets[row].append(color.verifyColor(row, column, result_combined,
															   result_white, result_red, result_orange,
															   result_yellow, result_green, result_blue
															   ))
				cv2.imwrite("image_resized.jpg", result_final)
				print(str(cubelets[0]))
				print(str(cubelets[1]))
				print(str(cubelets[2]))
				cubelets_list.append(cubelets)
				for_kociemba = str(cubelets_list)
				for_kociemba = for_kociemba.translate(str.maketrans('', '', string.punctuation))
				for_kociemba = (for_kociemba.replace(' ', ''))
				print(for_kociemba)
				algorithm = kociemba.solve(for_kociemba)
				print (for_kociemba)
				print (algorithm)
				print (image_no)

	#audio.outputAudioTurns(n)
	print("Outputting signal for " + str(n) + " seconds")
	#cv2.destroyAllWindows()	# With everything done, release capture
	print("Done!")
main()