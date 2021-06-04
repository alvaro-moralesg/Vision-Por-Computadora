import cv2
import numpy as np
import p6A as tf
import os

img_o = cv2.imread('../ascii.jpg')
img_d = img_o.copy()
img_slct = None
slct_flag = False
drawing = False 
ix , iy = -1 , -1

def slct_check(event, x, y, flags, param):
    global slct_flag
    if slct_flag == False:
        slct (event, x, y, flags, param)

def slct (event, x, y, flags, param):
    global img_o, img_d, img_slct, slct_flag, drawing, ix, iy
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix , iy = x , y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True :
            img_d = img_o.copy()
            cv2.rectangle(img_d, (ix, iy), (x, y), (0, 255, 0), 0)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        slct_flag = True
        if ix <= x and iy <= y:
            img_slct = img_d[iy+1:y,ix+1:x]
        elif ix < x and iy > y:
            img_slct = img_d[y+1:iy,ix+1:x]
        elif ix > x and iy < y:
            img_slct = img_d[iy+1:y,x+1:ix]
        elif ix > x and iy > y:
            img_slct = img_d[y+1:iy,x+1:ix]
        print("Realizo una seleccion. Sobre la ventana presione: "
            "\n- 'g' para guardar la imagen seleccionada."
            "\n- 'e' para aplicar tranformacion euclidiana."
            "\n- 'r' para volver a seleccionar."
            "\n- 'q' para cerrar el programa.")
        

cv2.namedWindow('laven tana')
cv2.setMouseCallback('laven tana', slct_check)
print("Seleccionando imagen.")
while (1): 
    cv2.imshow('laven tana', img_d)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    elif slct_flag == True:
        if k == ord('r'):
            os.system('clear')
            print("Seleccionando imagen.")
            slct_flag = False
            img_d = img_o.copy()
        elif k == ord('g'):
            try:    
                cv2.imwrite('slct_figure.png', img_slct)
                print("Imagen seleccionada guardada como 'slct_figure.png'.")
            except: 
                print('Error al guardar la imagen. Intentar nuevamente.')           #Error que ocurre cuando se selecciona un punto o una linea
        elif k == ord('e'):
            img_transf =  tf.euc_s(img_slct)
            try:
                cv2.imwrite('tf_figure.png', img_transf)
                print("Imagen transformada guardada como 'tf_figure.png'")
            except:
                print('Error al guardar la imagen. Intentar nuevamente.')
    
cv2.destroyAllWindows()