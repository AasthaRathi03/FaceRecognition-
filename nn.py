import cv2

cap = cv2.VideoCapture("http://10.73.192.167:4747/video")

while True:
    ret, frame = cap.read()
    print(ret)

    if not ret:
        break

    cv2.imshow("Test", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()