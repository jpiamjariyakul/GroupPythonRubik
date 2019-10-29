import cv2
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime

def nothing(x):
    pass

cv2.namedWindow("Video Frame - Original", cv2.WINDOW_NORMAL)
# ^This creates a window, and cv2.imshow loads the video into it. It is only for resizing purposes. Works perfectly without

cv2.namedWindow("Trackbar")
cv2.createTrackbar("LH", "Trackbar", 0, 180, nothing)
cv2.createTrackbar("LS", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("LV", "Trackbar", 0, 255, nothing)
cv2.createTrackbar("UH", "Trackbar", 180, 180, nothing)
cv2.createTrackbar("US", "Trackbar", 255, 255, nothing)
cv2.createTrackbar("UV", "Trackbar", 255, 255, nothing)


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
#showImage(img_RGB, "insert cool title here")

def saveframe(frame, color):
    # Put here since function() that calls current time, NOT time of launch
    now = datetime.now()
    filename_date = str(now.year).zfill(4) + str(now.month).zfill(2) + str(now.day).zfill(2)
    filename_time = str(now.hour).zfill(2) + str(now.minute).zfill(2) + str(now.second).zfill(2)
    # Saves filename in sortable titles, i.e. yyyyMMdd_HHmmSS.jpg
    # Assumes 1 (or none) keystroke per second
    filename = filename_date + "_" + filename_time + "_" + str(color) + ".jpg"
    cv2.imwrite(filename, frame)
    print("Image saved as " + filename)

def main():
    # Takes snapshot of image & writes to file
    cap = cv2.VideoCapture(0) # 1 since webcam camera is used - 0 uses back camera

    # Confirms that camera is open
    if cap.isOpened() == False:
        print("cap not opened, opening cap")
        cap.open()

    while(True):
        # Captures frame-by-frame
        ret, frame = cap.read()
        Gaussian_filter = cv2.GaussianBlur(frame, (5, 5), 0)
        #gaussian filter is applied to remove noises

        # Operations on frame here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Converts color-space from BGR to HSV
        frame_hsv = cv2.cvtColor(Gaussian_filter, cv2.COLOR_BGR2HSV)
        # Adjusting threshold to find suitable HSV values

        lh = cv2.getTrackbarPos("LH", "Trackbar")
        ls = cv2.getTrackbarPos("LS", "Trackbar")
        lv = cv2.getTrackbarPos("LV", "Trackbar")
        uh = cv2.getTrackbarPos("UH", "Trackbar")
        us = cv2.getTrackbarPos("US", "Trackbar")
        uv = cv2.getTrackbarPos("UV", "Trackbar")


        # Defines boundaries in HSV for the color blue
        # blue_lower = np.array([110, 50, 50])
        # blue_upper = np.array([130, 255, 255])
        # blue_lower = np.array([101, 128, 128])
        # blue_upper = np.array([150, 255, 255])

        # In OpenCV, range is [179, 255, 255]

        # Defines boundaries in HSV for the color white
        white_lower = np.array([113, 0, 169])
        white_upper = np.array([163, 32, 249])
        # Defines boundaries in HSV for the color red
        red_lower = np.array([150, 100, 100])
        red_upper = np.array([180, 255, 255])
        # red_lower = np.array([151, 128, 128])
        # red_upper = np.array([180, 255, 255])
        # Defines boundaries in HSV for the color orange

        orange_lower = np.array([0, 40, 241])
        orange_upper = np.array([14, 255, 255])

        # Defines boundaries in HSV for the color yellow
        yellow_lower = np.array([20, 100, 100])
        yellow_upper = np.array([30, 255, 255])
        # Defines boundaries in HSV for the color green
        green_lower = np.array([40, 40, 40])
        green_upper = np.array([70, 255, 255])
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

        #boundary rules
        mask_together = mask_yellow + mask_red + mask_orange + mask_green + mask_blue + mask_white
        kernel = np.ones((5, 5), np.uint8)
        mask_together = cv2.erode(mask_together,  kernel)
        #eroding reduces noises
        #contours
        contours, _ = cv2.findContours(mask_together, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for count in contours:
            approx = cv2.approxPolyDP(count, 0.01*cv2.arcLength(count, True), True)
            area = cv2.contourArea(count)
            if area > 500:
                cv2.drawContours(Gaussian_filter, [count], 0, (0, 255, 0), 5)

        # Applies a bitwise-AND operation on the mask and original image
        result_white = cv2.bitwise_and(Gaussian_filter, Gaussian_filter , mask=mask_white)
        result_red = cv2.bitwise_and(Gaussian_filter, Gaussian_filter , mask=mask_red)
        result_orange = cv2.bitwise_and(Gaussian_filter, Gaussian_filter , mask=mask_orange)
        result_yellow = cv2.bitwise_and(Gaussian_filter, Gaussian_filter , mask=mask_yellow)
        result_green = cv2.bitwise_and(Gaussian_filter, Gaussian_filter , mask=mask_green)
        result_blue = cv2.bitwise_and(Gaussian_filter, Gaussian_filter , mask=mask_blue)
        result_final = cv2.bitwise_and(Gaussian_filter, Gaussian_filter, mask=mask_together)

        # Displays frame
        cv2.imshow("Video Frame - Original", Gaussian_filter)
        cv2.imshow("Video Frame - White", result_white)
        cv2.imshow("Video Frame - Red", result_red)
        cv2.imshow("Video Frame - Orange", result_orange)
        cv2.imshow("Video Frame - Yellow", result_yellow)
        cv2.imshow("Video Frame - Green", result_green)
        cv2.imshow("Video Frame - Blue", result_blue)
        cv2.imshow("Video Frame - final", result_final)

        # Recognises keystroke
        keystroke = cv2.waitKey(1) & 0xFF
        if keystroke == 27: # wait for ESC key to exit
            break
        elif (keystroke == ord('s')) or (keystroke == ord('S')): # wait for S/s key to save image
            #saveframe(frame, "Original")
            #saveframe(result_red, "Red")
            #saveframe(result_orange, "Orange")
            #saveframe(result_yellow, "Yellow")
            #saveframe(result_green, "Green")
            #saveframe(result_blue, "Blue")
            #saveframe(result_white, "White")
            saveframe(mask_together, "Final")

    # With everything done, release capture
    cap.release()
    cv2.destroyAllWindows()

main()
