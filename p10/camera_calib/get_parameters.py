import numpy as np
import cv2
import glob

def get_parameters():
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    objp = np.zeros((12,3), np.float32)
    objp [:,:2] = np.mgrid[0:4,0:3].T.reshape((-1,2))
    objpoints = []
    imgpoints = []
    images = glob.glob('camera_calib/tmp/*.jpg')
    for fname in images :
        print(fname)
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (4,3), None)
        if ret is True:
            # print('*')
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2) 
            # img = cv2.drawChessboardCorners(img, (4, 3),corners2,ret)
            # cv2.imshow('img',img)
            cv2.waitKey(300)
    cv2.destroyAllWindows()
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    return ret, mtx, dist, rvecs, tvecs