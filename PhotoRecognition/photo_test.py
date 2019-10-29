### Imports prerequisites & libraries
import cv2
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime


### Declares faces visible to camera & to be analysed
# Takes assumption that faces are labelled per following convention
'''
[			UP				]
[	LEFT	]	[   FRONT	]
'''
# Declares 3x3 tuple for storing pixel coordinates of face UP
coord_up =  (	
                (	( 96,	 96),	(123,	 86),	(148,	 76)	),
                (   (122,	107),	(150,	 96),	(175,	 85)	),
                (	(153,	120),	(181,	107),	(204,	 94)	)
            )
# Declares 3x3 tuple for storing pixel coordinates of face LEFT
coord_lf =  (
                (   ( 80,	115),	(107,	128),	(137,	141)	),
                (   ( 87,	137),	(110,	149),	(136,	163)	),
                (   ( 91,	155),	(112,	168),	(135,	181)	)
            )
# Declares 3x3 tuple for storing pixel coordinates of face FRONT
coord_fr =  (
                (	(169,	141),	(196,	128),	(218,	115)	),
                (   (165,	163),	(190,	149),	(213,	137)	),
                (   (163,	181),	(187,	168),	(209,	155)	)
            )


def nothing(x):
    pass

# Creates a resizable window frame - one loads video/image into it
cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
# Program functions perfectly normal w/out the 


def main():
    while(True):
        # Captures frame-by-frame
        frame = cv2.imread("image_01.jpg", cv2.IMREAD_COLOR)

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
        mask_white = cv2.inRange(frame_hsv, white_lower, white_upper) # Obtains white
        mask_red = cv2.inRange(frame_hsv, red_lower, red_upper) # Obtains red
        mask_orange = cv2.inRange(frame_hsv, orange_lower, orange_upper) # Obtains orange
        mask_yellow = cv2.inRange(frame_hsv, yellow_lower, yellow_upper) # Obtains yellow
        mask_green = cv2.inRange(frame_hsv, green_lower, green_upper) # Obtains green
        mask_blue = cv2.inRange(frame_hsv, blue_lower, blue_upper) # Obtains blue
        # Combines previous HSV masks together
        mask_combined = mask_yellow + mask_red + mask_orange + mask_green + mask_blue + mask_white
        
        # Sets erosion filter factor
        kernel = np.ones((5, 5), np.uint8)
        # Eroding reduces noise in image
        mask_combined = cv2.erode(mask_combined,  kernel)

        # Finds contours of image
        contours, _ = cv2.findContours(mask_combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Forms contours around lines
        for count in contours:
            # Question: what does this line do?
            approx = cv2.approxPolyDP(count, 0.1 * cv2.arcLength(count, True), True)
            area = cv2.contourArea(count)
            # Area factor of 500 selected - 
            if area > 500:
                cv2.drawContours(image_gaussian, [count], 0, (0, 255, 0), 2)

        # Applies a bitwise-AND operation on the combined mask and original (blurred) image
        result_final = cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_combined)
        # Resize image to normalised size, i.e. 300x300
        result_final = cv2.resize(result_final, (300, 300))
        # This allows for a normalised coordinate system afterwards
        # Such will be used during detecting each facelets, per each point in image

        # Displays image/video in frame
        cv2.imshow("Frame", result_final)

        
        # Recognises keystroke
        keystroke = cv2.waitKey(0) & 0xFF
        #if keystroke == 27: # wait for ESC key to exit
        if keystroke == ord('s'): # wait for ESC key to exit
            cv2.imwrite("image_resized.jpg", result_final)
            print("File written")
            break
        else:
            break
        

        # Waits until any key inputted -> terminates program
        # cv2.waitKey(0)
        # break

        """
        elif (keystroke == ord('s')) or (keystroke == ord('S')): # wait for S/s key to save image
            saveframe(result_final, "Final")
            '''
            saveframe(frame, "Original")
            saveframe(result_red, "Red")
            saveframe(result_orange, "Orange")
            saveframe(result_yellow, "Yellow")
            saveframe(result_green, "Green")
            saveframe(result_blue, "Blue")
            saveframe(result_white, "White")
            '''
        """

    # With everything done, release capture
    # cap.release()
    cv2.destroyAllWindows()

main()
