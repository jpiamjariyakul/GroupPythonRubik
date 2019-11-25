### Imports prerequisites & libraries
import cv2
import numpy as np

# Creates a resizable window frame - one loads video/image into it
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
# Program functions perfectly normal w/out line in

def main():
	"""Stage 1.1: Obtain masks for each individual color in image"""
	# Captures frame-by-frame
	frame = cv2.imread("C:\Users\jpiam\Documents\GitHub\RubikPython\PhotoRecognition\image02.jpg")

	while(True):
		# Displays image/video in frame
		cv2.imshow("Frame", frame)
		# Recognises keystroke
		keystroke = cv2.waitKey(0) & 0xFF
		#if keystroke == 27: # wait for ESC key to exit
		if keystroke == ord('s'): # wait for 's' key to save image
			cv2.imwrite("image_resized.jpg", result_final)
			print("File written")
			break
		else:
			break
	cv2.destroyAllWindows()

main()