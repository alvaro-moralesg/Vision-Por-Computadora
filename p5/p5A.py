import cv2
import numpy as np

def euc(img):
    print('Para aplicar la transformacion ingrese:')
    angle = float(input('Angulo de rotacion en grados: '))
    tx = int(input('Traslacion en eje x: '))
    ty = int(input('Traslacion en y: '))
    angle = np.pi * angle / 180 
    (h, w) = (img.shape[0], img.shape[1])
    M = np.float32([[np.cos(angle)   , np.sin(angle), tx],
                    [-1*np.sin(angle), np.cos(angle), ty]])
    np.set_printoptions(suppress=True)
    print('Matriz de transformacion\n', M)
    dst = cv2.warpAffine(img, M, (w, h))
    return dst