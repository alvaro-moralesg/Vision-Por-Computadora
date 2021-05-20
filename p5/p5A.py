import cv2
import numpy as np

def transf (img, angle = 60, tx = 0, ty = 0):
    angle = np.pi * angle / 180 
    (h, w) = (img.shape[0], img.shape[1])
    M = np.float32([[np.cos(angle)   , np.sin(angle), tx],
                    [-1*np.sin(angle), np.cos(angle), ty]])
    np.set_printoptions(suppress=True)
    print('Matriz de transformacion\n', M)
    dst = cv2.warpAffine(img, M, (w, h))
    return dst