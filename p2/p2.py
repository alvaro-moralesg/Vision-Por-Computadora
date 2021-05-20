# Crear un programa que lea una imagen en blanco y negro.
# Aplicar un umblar sobre los valores de los pixeles
# Guardar resultado
# No usar ninguna funcion de OpenCV, excepto leer y guardar

import cv2

img = cv2.imread('hoja.png', 0)

x , y = img . shape

for i in range(x):
    for j in range(y):
        if img[i,j] <= 100:
            img[i,j] = 0
        else:
            img[i,j] = 255
            
cv2.imwrite ('resultado.png',img)