#Detecta arucos y ubica una imagen sobre ellos. La idea final era poder ubicar imagenes sobre
#los parches de una bateria (imagen aruco_test1.jpg) para pobrar algunos diseños.
#Quedaria ampliar el tamaño de las imagenes que agrego y aplicar una mascara para borrarles el fondo.
#Comentando y descomentando algunas lineas puedo detectar arucos usando la camara o videos cargados.

import cv2 as cv
import numpy as np
import camera_calib.get_parameters as cp

#Cargamos el diccionario.
dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
#Creamos el detector
parameters = cv.aruco.DetectorParameters_create()

#Obtenemos la matriz de calib de la camara
cret, mtx, dist, rvecs, tvecs = cp.get_parameters()

#Cargamos la camara
# vd = cv.VideoCapture(0)

#Cargamos el video
vd = cv.VideoCapture('aruco_test.mp4')
fps = vd.get(5)

#Cargamos la imagen
ar_img = cv.imread('doge.png')

def img_insrt(corner, ids, frame, ar_img):
    imgout = 0
    h, w, c = ar_img.shape
    pts2 = np.float32([[0,0], [w,0], [w,h], [0,h]])
    for i in range(len(ids)):
        tl = corner[i][0][0]
        tr = corner[i][0][1]
        br = corner[i][0][2]
        bl = corner[i][0][3]
        pts1 = np.array([tl, tr, br, bl])
        matrix, _ = cv.findHomography(pts2, pts1)
        img_id = cv.warpPerspective(ar_img, matrix, (frame.shape[1], frame.shape[0]))
        cv.fillConvexPoly(frame, pts1.astype(int), (0, 0, 0))
        imgout += img_id
    imgout = imgout + frame
    return imgout


while ( 1 ) :
    vret, vframe = vd.read()
    #Detectamos los marcadores en la imagen
    corners , ids , rejected = cv.aruco.detectMarkers(vframe,dictionary,parameters=parameters)

    if ids is not None:
        #Obtengo la pose de los marcadores
        vrvecs, vtvecs, _ = cv.aruco.estimatePoseSingleMarkers(corners, 0.04, mtx, dist)

        #Aplico la imagen
        ar_img_t = img_insrt(corners, ids, vframe, ar_img)
        cv.imshow('ventana',ar_img_t)
    else:
        cv.imshow('ventana',vframe)
        
    key = cv.waitKey(50)
    if (key == 27):
        cv.destroyAllWindows()
        break
 

