
        # Gaussian filter is applied to captured image - remove noises
        image_gaussian = cv2.GaussianBlur(frame, (3, 3), 0)

        # Converts color-space from BGR to HSV
        frame_hsv = cv2.cvtColor(image_gaussian, cv2.COLOR_BGR2HSV)
        
        
        '''
        # Adjusting threshold to find suitable HSV values
        lh = cv2.getTrackbarPos("LH", "Trackbar")
        ls = cv2.getTrackbarPos("LS", "Trackbar")
        lv = cv2.getTrackbarPos("LV", "Trackbar")
        uh = cv2.getTrackbarPos("UH", "Trackbar")
        us = cv2.getTrackbarPos("US", "Trackbar")
        uv = cv2.getTrackbarPos("UV", "Trackbar")
        '''


        # In OpenCV, range is [179, 255, 255]
        # Defines boundaries in HSV for the color white
        white_lower = np.array([0, 0, 200])
        white_upper = np.array([179, 20, 255])
        # Defines boundaries in HSV for the color red
        red_lower = np.array([0, 132, 125])
        red_upper = np.array([9, 255, 255])
        # Defines boundaries in HSV for the color orange
        orange_lower = np.array([0, 77, 208])
        orange_upper = np.array([15, 255, 255])
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
            approx = cv2.approxPolyDP(count, 0.005 * cv2.arcLength(count, True), True)
            area = cv2.contourArea(count)
            # Area factor of 500 selected - 
            if area > 500:
                cv2.drawContours(image_gaussian, [count], 0, (0, 255, 0), 5)


        '''
        # Applies a bitwise-AND operation on the mask and original image
        result_white = cv2.bitwise_and(image_gaussian, image_gaussian , mask=mask_white)
        result_red = cv2.bitwise_and(image_gaussian, image_gaussian , mask=mask_red)
        result_orange = cv2.bitwise_and(image_gaussian, image_gaussian , mask=mask_orange)
        result_yellow = cv2.bitwise_and(image_gaussian, image_gaussian , mask=mask_yellow)
        result_green = cv2.bitwise_and(image_gaussian, image_gaussian , mask=mask_green)
        result_blue = cv2.bitwise_and(image_gaussian, image_gaussian , mask=mask_blue)#result_final = result_white + result_red + result_orange + result_yellow + result_green + result_blue
        '''

        # Applies a bitwise-AND operation on the combined mask and original (blurred) image
        result_final = cv2.bitwise_and(image_gaussian, image_gaussian, mask=mask_combined)


        '''
        # Displays frame
        cv2.imshow("Video Frame - Original", image_gaussian)
        cv2.imshow("Video Frame - White", result_white)
        cv2.imshow("Video Frame - Red", result_red)
        cv2.imshow("Video Frame - Orange", result_orange)
        cv2.imshow("Video Frame - Yellow", result_yellow)
        cv2.imshow("Video Frame - Green", result_green)
        cv2.imshow("Video Frame - Blue", result_blue)
        cv2.imshow("Video Frame - final", result_final)
        cv2.imshow("Video Frame - Original", result_final)
        '''

        
        # Displays image/video in frame
        cv2.imshow("Frame", result_final)

        # Recognises keystroke
        keystroke = cv2.waitKey(1) & 0xFF
        if keystroke == 27: # wait for ESC key to exit  
            cv2.destroyAllWindows()
            break
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
    #cv2.destroyAllWindows()