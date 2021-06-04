import cv2
import numpy as np
from numpy.lib.shape_base import get_array_prepare
import p7A as tf
import os

img_o = cv2.imread('../ascii.jpg')
img_d = img_o.copy()
img_slct = None
i_flag = False
drawing = False 
mode = 0
ix , iy = [], []

def slct_check(event, x, y, flags, param):
    global i_flag, mode
    if i_flag == False:
        if mode == 0:
            slct (event, x, y, flags, param)
        else:
            pt_slct(event, x, y, flags, param)

def slct (event, x, y, flags, param):
    global img_o, img_d, img_slct, i_flag, drawing, ix, iy
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix , iy = x , y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing is True :
            img_d = img_o.copy()
            cv2.rectangle(img_d, (ix, iy), (x, y), (0, 255, 0), 0)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        i_flag = True
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

def pt_slct(event, x, y, flags, param):
    global img_o, img_d, img_slct, i_flag, ix, iy
    if event == cv2.EVENT_LBUTTONDOWN:
        ix.append(x)
        iy.append(y)
        cv2.circle(img_d, (x,y), 5, (255, 0, 0), -1)
        if len(ix) == 3:
            i_flag = True
            img_insrt = cv2.imread('../boina.png')
            #Resize
            (h_o, w_o) = (img_o.shape[0], img_o.shape[1])
            img_insrt = cv2.resize(img_insrt, (w_o,w_o))
            #Transformacion
            img_insrt = tf.aff(img_insrt, ix, iy, h_o, w_o)
            #Mascara
            gray_img = cv2.cvtColor(img_insrt, cv2.COLOR_RGB2GRAY)
            _, mask = cv2.threshold(gray_img, 120, 255, cv2.THRESH_BINARY)
            fondo = cv2.bitwise_or(img_d, img_d, mask=mask)
            frente = cv2.bitwise_and(img_insrt, img_insrt, mask=cv2.bitwise_not(mask))
            img_d = cv2.add(fondo, frente)

cv2.namedWindow('laven tana')
cv2.setMouseCallback('laven tana', slct_check)

print('Seleccion de imagen por arrastre. Presione "a" para cambiar al modo de insercion de imagen.')
while (1): 
    cv2.imshow('laven tana', img_d)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    elif k == ord('r'):
        os.system('clear')
        if mode == 1:
            print('Modo de insercion de imagen. Seleccione 3 puntos.')
        else:
            print('Modo de seleccion por arrastre.')
        ix = []
        iy = []
        i_flag = False
        img_d = img_o.copy()
    elif k == ord('a'):
        if i_flag == True:
            print('Vuelva la imagen a su estado original pulsando "r"')
        else:
            if mode != 1:
                print('Cambio al modo de insercion de imagen. Seleccione 3 puntos.')
                mode = 1
            else:
                print('Cambio al modo de seleccion por arrastre.')
                mode = 0
    elif i_flag == True and mode == 0:
        if k == ord('g'):
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