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
    np.set_printoptions(precision=3,suppress=True)
    print('Matriz de transformacion\n', M)
    dst = cv2.warpAffine(img, M, (w,h))
    return dst

def aff (img, ix, iy, h_0, w_o):
    src_img_insrt = np.array([ [0,0], [w_o,0], [0, w_o-1] ]).astype(np.float32)
    dst_img_insrt = np.array([ [ix[0], iy[0]], [ix[1], iy[1]], [ix[2], iy[2]] ]).astype(np.float32)
    M = cv2.getAffineTransform(src_img_insrt, dst_img_insrt)
    return cv2.warpAffine(img, M, (w_o, h_0), borderValue = (255, 255, 255))

def rect (img, ix, iy):
    ix_dist = [abs(ix[0]-ix[idx]) for idx in range(4)]
    iy_dist = [abs(iy[0]-iy[idx]) for idx in range(4)]
    ix_max = max(ix_dist)
    iy_max = max(iy_dist)
    src_coord = np.array([ [ix[idx], iy[idx]] for idx in range(4) ]).astype(np.float32)
    dst_coord = np.array([ [0,0], [ix_max,0], [0,iy_max], [ix_max,iy_max]  ]).astype(np.float32)
    M = cv2.getPerspectiveTransform(src_coord,dst_coord)
    return cv2.warpPerspective(img, M, (ix_max,iy_max))