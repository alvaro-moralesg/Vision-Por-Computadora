import cv2
import numpy as np

def persp_tf (img, x, y, ratio):
    ix_dist = max([abs(x[0]-x[idx]) for idx in range(4)])
    iy_dist = ix_dist * ratio
    src_coord = np.array([ [x[idx], y[idx]] for idx in range(4) ]).astype(np.float32)
    dst_coord = np.array([ [x[0],y[0]]          , [x[0]+ix_dist,y[0]] , 
                           [x[0],y[0]+iy_dist]  , [x[0]+ix_dist,y[0]+iy_dist] 
                        ]).astype(np.float32)
    M = cv2.getPerspectiveTransform(src_coord,dst_coord)
    return cv2.warpPerspective(img, M, (img.shape[1],img.shape[0])) , ix_dist , iy_dist

def new_scale(img,maxW,maxH):
    ratio = min(maxW/img.shape[1],maxH/img.shape[0])
    newS = ( int(img.shape[1]*ratio) , int(img.shape[0]*ratio) )
    return cv2.resize(img, newS, cv2.INTER_AREA) 
