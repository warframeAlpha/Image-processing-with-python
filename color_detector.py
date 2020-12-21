import numpy as np
import cv2

input_photo = cv2.imread('') #輸入裁切且轉正的照片的路徑(資料夾分隔要用"/")
original_image = cv2.imread('')#輸入原本的影像的路徑
[l, w] = [15,15] # 輸入垂直的長,橫的寬，單位一致就好
[xres_photo, yres_photo] = [l/input_photo.shape[0],w/input_photo.shape[0]] # l,w除以格子數 = 每格多長 (照片解析度)
[xres_image, yres_image] = [l/original_image.shape[0],w/original_image.shape[1]] # (原始影像解析度)

## 對 原始影像down sample，使解析度一致


