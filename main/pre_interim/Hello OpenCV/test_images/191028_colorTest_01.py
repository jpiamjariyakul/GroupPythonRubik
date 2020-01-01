# Rubik's Cube Project - Color Detection Test
# Start: 2019-010-28
# End: Ongoing
# By Jay Piamjariyakul

# Utilises materials from the following link:
## https://programmablebrick.blogspot.com/2017/02/rubiks-cube-tracker-using-opencv.html

# 0 - Prerequisites
# Imports prerequisite libraries/modules
import cv2
import numpy as np

# Sets path to file to be tested, in this case face_singular.jpg
filename = "face_singular.jpg"

## ------------------------------------

# 1 - Canny Edge Detection
# := Detects edge of objects in diagram
# Initial image processing per follows:
# Loads image -> Greyscale -> Gaussian blur -> Canny
# Greyscaling allows image edges to be more easily detected, compared to coloured where too many information persists
# Gaussian blur removes noise in image & only retains necessary information

img_cube_original = cv2.imread(filename)
img_cube_grey_unblurred = cv2.cvtColor(img_cube_original, cv2.COLOR_BGR2GRAY)
img_cube_grey_blurred = cv2.GaussianBlur(img_cube_grey_unblurred, (3, 3), cv2.BORDER_DEFAULT)
img_cube_canny = cv2.Canny(img_cube_grey_blurred, 20, 40)

# 2 - Line Dilation
# := Increases thickness of detected edges -> alleviates contour detection of squares
kernel = np.ones((3,3), np.uint8) # Forms 3x3 matrix of 1s
# Increases thickness by two pixels <- due to iterations
img_cube_dilated = cv2.dilate(img_cube_canny, kernel, iterations=2)

# 3 - Contour Detection
# := OpenCV finding "a curve joining all the continuous points (along the boundary), having same color or intensity"
(contours, hierarchy) = cv2.findContours(img_cube_dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

while(True):
    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
    cv2.imshow("frame", img_cube_dilated)
    keystroke = cv2.waitKey(1) & 0xFF
    if keystroke == 27: # wait for ESC key to exit
        break

cv2.destroyAllWindows()