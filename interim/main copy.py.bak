### Imports prerequisites & libraries
import cv2

# Creates a resizable window frame - one loads video/image into it
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
# Program functions perfectly normal w/out line in

def main():
	"""Stage 1.1: Obtain masks for each individual color in image"""
	#frame = cv2.imread("image_02.jpg", cv2.IMREAD_COLOR)	# Captures frame-by-frame
	cap = cv2.VideoCapture(1)
	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()
		frame = cv2.resize(frame, (300, 300))

		keystroke = cv2.waitKey(1) & 0xFF	# Recognises keystroke
		cv2.imshow("Frame", frame)
		if keystroke == ord('s'): # wait for 's' key to save image
			break
	cap.release
	cv2.destroyAllWindows()	# With everything done, release capture
main()