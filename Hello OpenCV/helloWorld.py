import cv2
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime

# Uses MatPlotLib for showing images
def showImage(img, title):
    plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
    plt.title(title)
    plt.xticks([]), plt.yticks([])  # Hides tick values on X and Y axis
    plt.show()

# Opens window with image from directory
#img_BGR = cv2.imread("Clifton_Suspension_Bridge.jpg", cv2.IMREAD_COLOR)
#img_RGB = cv2.cvtColor(img_BGR, cv2.COLOR_BGR2RGB)
# Calls function to show image, inputting image and title as parameters
#showImage(img_RGB, "nsert cool title here")

def saveframe(frame):
    # Put here since function() that calls current time, NOT time of launch
    now = datetime.now()
    filename_date = str(now.year).zfill(4) + str(now.month).zfill(2) + str(now.day).zfill(2)
    filename_time = str(now.hour).zfill(2) + str(now.minute).zfill(2) + str(now.second).zfill(2)
    # Saves filename in sortable titles, i.e. yyyyMMdd_HHmmSS.jpg
    # Assumes 1 (or none) keystroke per second
    filename = filename_date + "_" + filename_time + ".jpg"
    cv2.imwrite(filename, frame)
    print("Image saved as " + filename)

def main():
    # Takes snapshot of image & writes to file
    cap = cv2.VideoCapture(1) # 1 since webcam camera is used - 0 uses back camera

    # Confirms that camera is open
    if cap.isOpened() == False:
        print("cap not opened, opening cap")
        cap.open()

    while(True):
        # Captures frame-by-frame
        ret, frame = cap.read()

        # Operations on frame here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Converts color-space from BGR to HSV
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Defines boundaries in HSV for the color blue
        # blue_lower = np.array([110, 50, 50])
        # blue_upper = np.array([130, 255, 255])

        # In OpenCV, range is [179, 255, 255]

        # Defines boundaries in HSV for the color blue
        blue_lower = np.array([50, 100, 100])
        blue_upper = np.array([70, 255, 255])

        # Sets threshold to the HSV image - obtains only blue colors
        mask_blue = cv2.inRange(frame_hsv, blue_lower, blue_upper)

        # Applies a bitwise-AND operation on the mask and original image
        result_blue = cv2.bitwise_and(frame, frame , mask=mask_blue)

        # Displays frame
        cv2.imshow("Video Frame", result_blue)

        # Recognises keystroke
        keystroke = cv2.waitKey(1) & 0xFF
        if keystroke == 27: # wait for ESC key to exit
            break
        elif (keystroke == ord('s')) or (keystroke == ord('S')): # wait for S/s key to save image
            saveframe(frame)

    # With everything done, release capture
    cap.release()
    cv2.destroyAllWindows()

main()
