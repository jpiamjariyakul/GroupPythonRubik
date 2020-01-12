import numpy as np
import cv2

cap = cv2.VideoCapture(1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    red_pixel = (0, 0, 255)
    # Our operations on the frame come here
    img = cv2.circle(frame, (200, 120), 10, (red_pixel), -1)
    img = cv2.circle(frame, (200, 240), 10, (red_pixel), -1)
    img = cv2.circle(frame, (200, 360), 10, (red_pixel), -1)
    img = cv2.circle(frame, (320, 120), 10, (red_pixel), -1)
    img = cv2.circle(frame, (320, 240), 10, (red_pixel), -1)
    img = cv2.circle(frame, (320, 360), 10, (red_pixel), -1)
    img = cv2.circle(frame, (440, 120), 10, (red_pixel), -1)
    img = cv2.circle(frame, (440, 240), 10, (red_pixel), -1)
    img = cv2.circle(frame, (440, 360), 10, (red_pixel), -1)



    # Display the resulting frame
    frame = cv2.resize(frame, (300, 300))
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()