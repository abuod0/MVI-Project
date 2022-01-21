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
#dilated = cv2.dilate(canny_edges, (4, 4), iterations=1)
#contours,h = cv2.findContours(canny_edges,2,2)

#$contours, hierarchy = cv2.findContours(bin_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

contours, hierarchy4 = cv2.findContours(canny_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    cv2.drawContours(img, [approx], 0, (0,255, 0), 2)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 5

    x1, y1, w, h = cv2.boundingRect(approx)
    aspectRatio = float(w) / h
    print(aspectRatio)

    if len(approx) == 10:
        cv2.putText(img, "Cap Nut", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    if aspectRatio >= 0.95 and aspectRatio <= 1.05:
        cv2.putText(img, "Flange Nut", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    elif len(approx) >= 15:
        if aspectRatio >= 0.1:
              cv2.putText(img, "Wing", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))




    # if len(approx) == 3:
    #
    #     cv2.putText(img, "Pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    # elif len(approx) == 10:
    #     cv2.putText(img, "Star", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
    # else:
    #     cv2.putText(img, "Circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

    #cv2.drawContours(img,[approx],0,(0,255,255),2)

    #cv2.drawContours(image=img, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    #cv2.drawContours(img, cnt, -1, (0, 255, 0), 2)

    #cv2.drawContours(img, [cnt], -1, (255, 0, 255), 2)

#print("Numer of Nuts: ", len(cnt))

print("Number of Nuts = " + str(len(contours)))

cv2.putText(img, "Number of Nuts = " + str(len(contours)),(10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
cv2.imshow('thresh', thresh)
cv2.imshow('binary', bin_img)
#cv2.imshow('sharpened image',sharpened)
cv2.imshow('blurred', blur)
cv2.imshow ('original', img)
cv2.imshow('Canny',canny_edges)

cv2.waitKey(0)
cv2.destroyAllWindows()
