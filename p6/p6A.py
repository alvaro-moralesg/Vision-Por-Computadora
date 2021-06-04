import cv2
import numpy as np

def euc_s(img):
    print('Para aplicar la transformacion ingrese:')
    angle = float(input('Angulo de rotacion en grados: '))
    s = float(input('Constante de escalado: '))
    tx = int(input('Traslacion en eje x: '))
    ty = int(input('Traslacion en y: '))
    angle = np.pi * angle / 180 
    (h, w) = (img.shape[0], img.shape[1])
    M = np.float32([[s*np.cos(angle)   , s*np.sin(angle), tx],
                    [-1*s*np.sin(angle), s*np.cos(angle), ty]])
    np.set_printoptions(suppress=True)
    print('Matriz de transformacion\n', M)
    dst = cv2.warpAffine(img, M, (w,h))
    return dst