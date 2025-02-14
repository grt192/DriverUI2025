import cv2
#camURl = "http://10.1.92.2:1181/stream.mjpg"
vidCap = cv2.VideoCapture(0)
while True:
    ret, frame = vidCap.read()
    cv2.imshow('frame', frame)
    cv2.waitKey(1)