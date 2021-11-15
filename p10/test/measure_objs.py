#Primera idea del practico. Decidi cambiarla por algo que necesite de la calibracion de la camara.
import cv2 as cv
import numpy as np


#Cargamos el diccionario de arucos y creamos el detector
dictionary = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
parameters = cv.aruco.DetectorParameters_create()
ar_side_cm = 4

#Creamos la camara
cam = cv.VideoCapture(0)

#Detector de objetos
def detector(frame):
        # Frame en escala de grises
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Mascara de threshold adaptativo
        #  cv.THRESH_BINARY_INV: si el pixel es mayor al threshold, se lo setea en 0
        #  cv.ADAPTIVE_THRESH_MEAN_C: el thresohld depende de la media de valores de un bloque de pixeles menos C
        C = 5
        block = 19
        mask = cv.adaptiveThreshold(gray, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY_INV, block, C)

        # Buscamos contornos
        #  cv.RETR_EXTERNAL: solo contornos externos
        #  cv.CHAIN_APPROX_SIMPLE: algoritmo de aproximacion simple
        contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        #cv.imshow("mask", mask)
        objects_contours = []

        for i in contours:
            area = cv.contourArea(i)
            if area > 2000:
                #i = cv.approxPolyDP(i, 0.03*cv.arcLength(i, True), True)
                objects_contours.append(i)

        return objects_contours

def dibujar_contorno(frame, contours):
    for i in contours:
        #Buscamos el rectangulo que forma el contorno del objeto
        rect = cv.minAreaRect(i)
        (x, y), (w, h), angle = rect
        #Obtenemos los vertices del rectangulo
        box = cv.boxPoints(rect)
        box = np.int0(box)
        #Centro del rectangulo
        cv.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
        #Dibujamos el contorno
        cv.polylines(frame, [box], True, (255, 0, 0), 2)
        return frame


while 1:
    #Capturamos un frame
    cret, cframe =  cam.read()
    #Detectamos aruco
    corners , ids , rejected = cv.aruco.detectMarkers(cframe,dictionary,parameters=parameters)
    if ids is not None:
        #Dibujamos contorno de aruco
        int_corners = np.int0(corners)
        cv.polylines(cframe, int_corners, True, (0, 255, 0), 2)
        #Conversion de pixeles a cm
        # Aruco Perimeter
        aruco_perim = cv.arcLength(corners[0], True)
        # Pixel to cm ratio
        px_cm_ratio = aruco_perim / (ar_side_cm*4)

        #Deteccion de objeto
        contours = detector(cframe)
        if contours is not None:
            #Dibujamos bordes de objeto
            cframe = dibujar_contorno(cframe, contours)
            
            for i in contours:
                #Obtenemos el ancho y alto del rectangulo que representa al objeto
                rect = cv.minAreaRect(i)
                (x, y), (w, h), angle = rect
                #Aplicamos el pixel ratio al ancho y alto del objeto en pixeles para obtener
                #las medidas en cm
                obj_w = w / px_cm_ratio
                obj_h = h / px_cm_ratio
                cv.putText(  cframe, "Ancho {} cm".format(round(obj_w, 1)),
                             (int(x - 100), int(y - 20)), cv.FONT_HERSHEY_PLAIN, 
                             2, (100, 200, 0), 2  )
                cv.putText(cframe, "Alto {} cm".format(round(obj_h, 1)),
                             (int(x - 100), int(y + 15)), cv.FONT_HERSHEY_PLAIN, 
                             2, (100, 200, 0), 2)
    cv.imshow('Camara',cframe)
    key = cv.waitKey(50)
    if (key == 27):
        cv.destroyAllWindows()
        break

