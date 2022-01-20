import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

height=350
width=350

dim = (width, height)
img1 = cv2.imread('111.jpg')
img= cv2.resize(img1, dim)
#sharpened=cv2.filter2D(img,-1,kernel_sharpening)

blur=cv2.blur(img,(2,2))
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

#flag, thresh = cv2.threshold(gray, 253, 255, cv2.THRESH_BINARY)
ret,thresh = cv2.threshold(gray,250,254,3)
ret, bin_img = cv2.threshold(thresh, 250, 255, cv2.THRESH_BINARY_INV)
canny_edges = cv2.Canny(bin_img, 250, 255)
dilated = cv2.dilate(canny_edges, (4, 4), iterations=1)
#contours,h = cv2.findContours(canny_edges,2,2)

#$contours, hierarchy = cv2.findContours(bin_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

contours, hierarchy4 = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)
for cnt in contours:
    cv2.drawContours(img,[cnt],0,(0,255,255),2)

    #cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    #cv2.drawContours(img, cnt, -1, (0, 255, 0), 2)

    #cv2.drawContours(img, [cnt], -1, (255, 0, 255), 2)

#print("Numer of Nuts: ", len(cnt))

print("Number of Nuts = " + str(len(contours)))

cv2.imshow('thresh', thresh)
cv2.imshow('binary', bin_img)
#cv2.imshow('sharpened image',sharpened)
cv2.imshow('blurred', blur)
cv2.imshow ('original', img)
cv2.imshow('Canny',canny_edges)

cv2.waitKey(0)
cv2.destroyAllWindows()
