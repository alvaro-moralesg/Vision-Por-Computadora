import sys
import cv2
import time

if len (sys.argv) >= 1 :
    filename = sys.argv[1]
else:
    print ('Pasar el nombre del video como argumento ')
    sys.exit(0)

cap = cv2.VideoCapture(filename)
fps = cap.get(5)
alto = int(cap.get(4))
ancho = int(cap.get(3))

fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
out = cv2.VideoWriter('output.avi', fourcc, fps, (alto, ancho)) 

while cap.isOpened() :
    ret, frame = cap.read()
    if ret is True :
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out.write(gray)
        cv2.imshow('Image gray', gray) 
    if (cv2.waitKey(int(fps)) & 0xFF) == ord ('q') :
        break

cap.release()
cv2.destroyAllWindows()