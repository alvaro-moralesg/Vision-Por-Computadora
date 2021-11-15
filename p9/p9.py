#

import cv2
import numpy as np
import funciones as tf

fname = 'figure.jpg'
img_o = cv2.imread(fname)
#Reduzco la escala de la imagen
img_o = tf.new_scale(img_o,1366, 768)
img_d = img_o.copy()
working_img = None
ix , iy = [], []
#Mediciones del rectangulo en referencia.jpg
sample_dim = (0.865,1.38) #(y,x)
sample_ratio = sample_dim[0] / sample_dim[1] #(y/x)
#font = cv2.FONT_HERSHEY_SIMPLEX

def open_window(window_num):
    window_name = 'Window '+str(window_num)
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) != 1:
        cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, set_points)
    return window_name

def set_points(event, x, y, flags, param):
    global ix, iy, working_img
    if event == cv2.EVENT_LBUTTONDOWN:
        ix.append(x)
        iy.append(y)
        cv2.circle(working_img, (x,y), 3, (255, 0, 0), -1)
        #cv2.putText(working_img, str(x) + ',' + str(y) , (x-10,y-10), font, 1,(0,0,255), 1, cv2.LINE_AA)

working_img = img_d
window_num = 1
working_window = open_window(window_num)
print('Seleccionar cuatro vertices.\n')
print('Presionar r para resetear puntos.')
flag_new_window = 1

while 1:

    k = cv2.waitKey(1) & 0xFF
    if k == ord('r'):
        if window_num == 1:
            ix = []
            iy = []
            working_img = img_o.copy()
        elif window_num == 2:
            working_img = img_persp_tf.copy()
            ix = []
            iy = []

    elif k == ord('q'):
        if window_num == 1:
            break
        elif window_num == 2:
            cv2.destroyWindow(working_window)
            working_img = img_d.copy() 
            window_num = 1
            working_window = open_window(window_num)
            flag_new_window = 1

    if window_num == 1:
        if flag_new_window:
            print('Trabajando en: '+working_window)
            flag_new_window = 0
        cv2.imshow(working_window,working_img)
        if len(ix) == 4:
            #Aplico trnasformacion, obtengo imagen transformada y distancia en pixeles de la referencia
            img_persp_tf, xdist_px, ydist_px = tf.persp_tf(img_o.copy(), ix, iy, sample_ratio)

            # cv2.imwrite('persp_tf_figure.png',img_persp_tf)
            #Antes de abrir una ventana nueva con la imagen transformada, guardo una copia de la actual
            img_d = working_img.copy()

            #Duplico la imagen transformada
            working_img = img_persp_tf.copy()
            
            #Cambio de ventana
            window_num = 2
            working_window = open_window(window_num)
            flag_new_window = 1
            ix = []
            iy = []
    if window_num == 2:
        if flag_new_window:
            print('Trabajando en: '+working_window)
            flag_new_window = 0
        cv2.imshow(working_window,working_img)
        if len(ix) == 2:
            #Dibujo lineas con flechas sobre los puntos de medicion
            cv2.arrowedLine(working_img, (ix[-1],iy[-1]), (ix[-2],iy[-2]), (170,0,170), 2)
            cv2.arrowedLine(working_img, (ix[-2],iy[-2]), (ix[-1],iy[-1]), (170,0,170), 2)

            #Obtengo relacion de pixeles y metros
            x_mt_px =  sample_dim[1] / xdist_px
            y_mt_px =  sample_dim[0] / ydist_px

            #Obtengo la distancia en metros
            x_dist = abs(ix[-1]-ix[-2])*x_mt_px
            y_dist = abs(iy[-1]-iy[-2])*y_mt_px
            dist = np.sqrt( pow(x_dist,2) + pow(y_dist,2) )
            print(str(dist)+'mts.')
            ix = []
            iy = []

cv2.destroyAllWindows()

