import cv2

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")



while True:
    ret, frame = cap.read()
    
    rval_left, left = cap.retrieve(0)
    rval_right, right = cap.retrieve(1)
    cv2.imshow("right", right)
    cv2.imshow("left", left)

    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()