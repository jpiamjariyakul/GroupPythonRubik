import cv2
import numpy as np
from matplotlib import pyplot as plt
from datetime import datetime

# Tuple storing pixels to check in image - amended later to accommodate rig
# NB: OpenCV uses a (Y,X) coordinate system
coord_yx = (
    (  # Pixels on face UP
        ((96, 96), (86, 123), (76, 148)),
        ((107, 122), (96, 150), (85, 175)),
        ((120, 153), (107, 181), (94, 204))
    ),
    (  # Pixels on face LEFT
        ((115, 80), (128, 107), (141, 137)),
        ((137, 87), (149, 110), (163, 136)),
        ((155, 91), (168, 112), (181, 135))
    ),
    (  # Pixels on face FRONT
        ((141, 169), (128, 196), (115, 218)),
        ((163, 165), (149, 190), (137, 213)),
        ((181, 163), (168, 187), (155, 209))
    )
)


def nothing(x):
    pass


# Defines color at coordinates given
def checkColor(hsv_combined,
               hsv_white, hsv_red, hsv_orange,
               hsv_yellow, hsv_green, hsv_blue):
    # Only uses array values & not the images themselves
    if np.any(hsv_combined == hsv_blue):
        return "B"
    elif np.any(hsv_combined == hsv_white):
        return "W"
    elif np.any(hsv_combined == hsv_red):
        return "R"
    elif np.any(hsv_combined == hsv_orange):
        return "O"
    elif np.any(hsv_combined == hsv_yellow):
        return "Y"
    elif np.any(hsv_combined == hsv_green):
        return "G"


# Verifies color at pixel & its surroundings whether it's black or otherwise
def verifyColor(face, row, column, c_combined,
                c_white, c_red, c_orange,
                c_yellow, c_green, c_blue):
    coord_row, coord_col = coord_yx[face][row][column][0], coord_yx[face][row][column][1]
    print(
        "XY [" + str(face) + " " + str(row) + " " + str(column) + "]: (" + str(coord_row) + ", " + str(coord_col) + ")")
    print("Found on first attempt: " + str(np.any(c_combined[coord_row][coord_col] != 0)))
    # Check if at specified coords there are colors
    if np.any(c_combined[coord_row][coord_col] != 0):
        # color = checkColor(	(coord_row + j), (coord_col + i), \
        # 							c_combined, \
        # 							c_white, c_red, c_orange, \
        # 							c_yellow, c_green, c_blue)
        # Passes HSV values instead of the images
        color = checkColor(c_combined[coord_row][coord_col], \
                           c_white[coord_row][coord_col], \
                           c_red[coord_row][coord_col], \
                           c_orange[coord_row][coord_col], \
                           c_yellow[coord_row][coord_col], \
                           c_green[coord_row][coord_col], \
                           c_blue[coord_row][coord_col])
        print("Color at (" + str(coord_row) + ", " + str(coord_col) + "): " + str(color))
        print("------------------------")
    else:  # Otherwise, iterate through 2 layers	until color found, or error
        layerMax = 3  # Max number of iterational layers to expand from original point
        i = j = -1 * layerMax
        i_initial = i
        while (True):
            if np.any(c_combined[coord_row + j][coord_col + i] != 0) and (i != 0) and (j != 0):
                color = checkColor(c_combined[coord_row + j][coord_col + i], \
                                   c_white[coord_row + j][coord_col + i], \
                                   c_red[coord_row + j][coord_col + i], \
                                   c_orange[coord_row + j][coord_col + i], \
                                   c_yellow[coord_row + j][coord_col + i], \
                                   c_green[coord_row + j][coord_col + i], \
                                   c_blue[coord_row + j][coord_col + i])
                print("Color at (" + str(coord_row + j) + ", " + str(coord_col + i) + "): " + str(color))
                print("------------------------")
                break
            else:
                print("!!! - Invalid color at " + str(coord_row + j) + ", " + str(coord_col + i) + " - adding range")
                if i >= layerMax:
                    i = i_initial
                    j += 1
                else:
                    i += 1
                if j >= layerMax:
                    color = "U"
                    print("ERROR - color undefined")
                    print("------------------------")
                    break
    return color


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
    plt.imshow(img, cmap='gray', interpolation='bicubic')
    plt.title(title)
    plt.xticks([]), plt.yticks([])  # Hides tick values on X and Y axis
    plt.show()


def main():
    # Takes snapshot of image & writes to file
    cap = cv2.VideoCapture(1)  # 1 since webcam camera is used - 0 uses back camera
    image_no = 0
    # Confirms that camera is open
    if cap.isOpened() == False:
        print("cap not opened, opening cap")
        cap.open()

    while (True):
        # Captures frame-by-frame

        ret, frame = cap.read()
        image_gaussian = cv2.GaussianBlur(frame, (5, 5), 0)
        # canny_edge = cv2.Canny(image_gaussian, 100, 150)
        # cv2.imshow("canny", canny_edge)
        # gaussian filter is applied to remove noises

        # Operations on frame here
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Converts color-space from BGR to HSV
        frame_hsv = cv2.cvtColor(image_gaussian, cv2.COLOR_BGR2HSV)
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
        white_lower = np.array([117, 21, 123])
        white_upper = np.array([145, 137, 204])
        # white_lower = np.array([lh, ls, lv])
        # white_upper = np.array([uh, us, uv])
        # Defines boundaries in HSV for the color red
        red_lower = np.array([0, 132, 125])
        red_upper = np.array([180, 255, 255])
        # red_lower = np.array([lh, ls, lv])
        # red_upper = np.array([uh, us, uv])
        # Defines boundaries in HSV for the color orange

        orange_lower = np.array([0, 77, 208])
        orange_upper = np.array([15, 255, 255])
        # orange_lower = np.array([lh, ls, lv])
        # orange_upper = np.array([uh, us, uv])

        # Defines boundaries in HSV for the color yellow
        yellow_lower = np.array([25, 60, 141])
        yellow_upper = np.array([65, 255, 255])
        # yellow_lower = np.array([lh, ls, lv])
        # yellow_upper = np.array([uh, us, uv])
        # Defines boundaries in HSV for the color green
        # green_lower = np.array([lh, ls, lv])
        # green_upper = np.array([uh, us, uv])
        green_lower = np.array([45, 53, 88])
        green_upper = np.array([91, 255, 255])
        # Defines boundaries in HSV for the color blue
        blue_lower = np.array([101, 128, 128])
        blue_upper = np.array([150, 255, 255])

        # Sets threshold to the HSV image
        mask_white = cv2.inRange(frame_hsv, white_lower, white_upper)  # Obtains white
        mask_red = cv2.inRange(frame_hsv, red_lower, red_upper)  # Obtains red
        mask_orange = cv2.inRange(frame_hsv, orange_lower, orange_upper)  # Obtains orange
        mask_yellow = cv2.inRange(frame_hsv, yellow_lower, yellow_upper)  # Obtains yellow
        mask_green = cv2.inRange(frame_hsv, green_lower, green_upper)  # Obtains green
        mask_blue = cv2.inRange(frame_hsv, blue_lower, blue_upper)  # Obtains blue

        # boundary rules
        mask_combined = mask_yellow + mask_red + mask_orange + mask_green + mask_blue + mask_white
        kernel = np.ones((5, 5), np.uint8)
        mask_combined = cv2.erode(mask_combined, kernel)
        # eroding reduces noises
        # contours
        contours, _ = cv2.findContours(mask_combined, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        #for count in contours:
            #approx = cv2.approxPolyDP(count, 0.01 * cv2.arcLength(count, True), True)
            #area = cv2.contourArea(count)
            #if area > 500:
                #cv2.drawContours(image_gaussian, [count], 0, (0, 255, 0), 5)

        # Applies a bitwise-AND operation on the combined mask and original (blurred) image
        result_final = cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_combined)
        # Resize image to normalised size, i.e. 300x300
        result_final = cv2.resize(result_final, (300, 300))
        # This allows for a normalised coordinate system afterwards
        # Such will be used during detecting each facelets, per each point in image

        # Resizes previous individual masks to allow color checking
        result_white = cv2.resize(
            cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_white),
            (300, 300)
        )
        result_red = cv2.resize(
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
        result_green = cv2.resize(
            cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_green),
            (300, 300)
        )
        result_blue = cv2.resize(
            cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_blue),
            (300, 300)
        )
        result_combined = result_white + result_red + result_orange + result_yellow + result_green + result_blue

        # Displays frame
        cv2.imshow("Video Frame - Original", image_gaussian)
        #cv2.imshow("Video Frame - White", result_white)
        #cv2.imshow("Video Frame - Red", result_red)
        #cv2.imshow("Video Frame - Orange", result_orange)
        #cv2.imshow("Video Frame - Yellow", result_yellow)
        #cv2.imshow("Video Frame - Green", result_green)
        #cv2.imshow("Video Frame - Blue", result_blue)
        #cv2.imshow("Video Frame - final", result_final)

        # Recognises keystroke
        keystroke = cv2.waitKey(1) & 0xFF

        if keystroke == 27:  # wait for ESC key to exit
            break
        elif (keystroke == ord('r')):
            image_no = 0
            print ("Image counter resetted")
        elif (keystroke == ord('s')) or (keystroke == ord('S')):  # wait for S/s key to save image
            #        ---------
            #        |       |
            #        |  U(1) |
            #        |       |
            # ----------------------------------
            # |      |       |        |        |
            # |  L(3)|  F(0) |   R(4) |   B(5) |
            # |      |       |        |        |
            #  ---------------------------------
            #        |       |
            #        |  D(2) |
            #        |       |
            #        ---------
            # Please snapshot each face of the cube in order of F->U->D->L->R->B with B being white
            print(image_no)
            if image_no == 0:
                filename = "F.png".format(image_no)
                cv2.imwrite(filename, frame)
                print("F face captured!".format(image_no))
                image_no += 1
                frame = cv2.imread("F.png", cv2.IMREAD_COLOR)
                # Defines individual faces & cubelets
                cubelets = []
                # Loop to fill all rows/columns
                for face in range(3):
                    cubelets.append([])  # Creates superlist for faces
                    for row in range(3):
                        cubelets[face].append([])  # Creates sublist for rows
                        for column in range(3):
                            cubelets[face][row].append(verifyColor(face, row, column, result_final,
                                                                   result_white, result_red, result_orange,
                                                                   result_yellow, result_green, result_blue
                                                                   ))
                print(str(cubelets[0][0]) + " | " + str(cubelets[1][0]) + " | " + str(cubelets[2][0]))
                print(str(cubelets[0][1]) + " | " + str(cubelets[1][1]) + " | " + str(cubelets[2][1]))
                print(str(cubelets[0][2]) + " | " + str(cubelets[1][2]) + " | " + str(cubelets[2][2]))


            elif image_no == 1:
                filename = "U.png".format(image_no)
                cv2.imwrite(filename, frame)
                print("Up face captured!".format(image_no))
                image_no += 1
                frame = cv2.imread("U.png", cv2.IMREAD_COLOR)
                # Defines individual faces & cubelets
                cubelets = []
                # Loop to fill all rows/columns
                for face in range(3):
                    cubelets.append([])  # Creates superlist for faces
                    for row in range(3):
                        cubelets[face].append([])  # Creates sublist for rows
                        for column in range(3):
                            cubelets[face][row].append(verifyColor(face, row, column, result_final,
                                                                   result_white, result_red, result_orange,
                                                                   result_yellow, result_green, result_blue
                                                                   ))
                print(str(cubelets[0][0]) + " | " + str(cubelets[1][0]) + " | " + str(cubelets[2][0]))
                print(str(cubelets[0][1]) + " | " + str(cubelets[1][1]) + " | " + str(cubelets[2][1]))
                print(str(cubelets[0][2]) + " | " + str(cubelets[1][2]) + " | " + str(cubelets[2][2]))



            elif image_no == 2:
                filename = "D.png".format(image_no)
                cv2.imwrite(filename, frame)
                print("Down face captured!".format(image_no))
                image_no += 1


            elif image_no == 3:
                filename = "L.png".format(image_no)
                cv2.imwrite(filename, frame)
                print("Left face captured!".format(image_no))
                image_no += 1


            elif image_no == 4:
                filename = "R.png".format(image_no)
                cv2.imwrite(filename, frame)
                print("Right face captured!".format(image_no))
                image_no += 1


            elif image_no == 5:
                filename = "B.png".format(image_no)
                cv2.imwrite(filename, frame)
                print("Back face captured!".format(image_no))
                image_no += 1


        elif (keystroke == ord('a')):

            print("exit")

    # With everything done, release capture
    cap.release()
    cv2.destroyAllWindows()


main()
