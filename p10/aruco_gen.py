import cv2 as cv
import numpy as np
# Cargamos el diccionario predefinido
diccionario = cv.aruco.Dictionary_get(cv.aruco.DICT_6X6_250)
# Generamos el marcador
imagen = np.zeros((200,200),dtype=np.uint8)
for i in range(5,13):
    imagen = cv.aruco.drawMarker(diccionario,i*5,200,imagen,1) 
    cv.imwrite ('markers/marker'+str(i*5)+'.png',imagen)

# Se agrego un margen a los arucos para mejorar la deteccion usando un codigo encontrado en:
# https://stackoverflow.com/questions/57845196/tune-of-aruco-detection-parameters-on-marker-identification