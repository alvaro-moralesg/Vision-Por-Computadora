#Este es un codigo con el que iba probando la camara y algunas lineas
#Esta super desprolijo
import cv2 
import numpy as np
import camera_calib.get_parameters as cp
import glob
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# objp = np.zeros((12,3), np.float32)
# objp [:,:2] = np.mgrid[0:4,0:3].T.reshape((-1,2))
# objpoints = []
# imgpoints = []
# Cargamos el diccionario.
dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
# Creamos el detector
parameters = cv2.aruco.DetectorParameters_create()

cret, mtx, dist, rvecs, tvecs = cp.get_parameters()

cap = cv2.VideoCapture(0)
j=0
while ( 1 ) :
    ret,frame = cap.read()
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #ret, corners = cv2.findChessboardCorners(gray, (4,3), None)
    corners , ids , rejected = cv2.aruco.detectMarkers(frame,dictionary,parameters=parameters)
    if ids is not None:
        #corners2 = cv2.cornerSubPix(frame, corners, (11, 11), (-1, -1), criteria)
        frame2 = frame.copy()
        rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(corners, 0.07, mtx, dist)
        for i in range(len(ids)):
            frame2 = cv2.aruco.drawAxis(frame2, mtx, dist, rvecs[i], tvecs[i], 0.12)
        # frame = cv2.drawChessboardCorners(frame, (4, 3),corners2,ret)
        # fname = 'tmp2/frame'+str(i)+'.jpg'
        # cv2.imwrite(fname,frame)
        # i+=1
        cv2.imshow("ventana",frame2)
    else:
        cv2.imshow("ventana",frame)
    key = cv2.waitKey(10)
    if (key == 27):
        break
    if key == ord(' '):
        fname = 'tmp2/frame'+str(j)+'.jpg'
        cv2.imwrite(fname,frame)
        j+=1

cv2.destroyAllWindows()