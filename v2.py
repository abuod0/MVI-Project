import cv2
import numpy as np
from time import sleep

min_width = 80
Height_min = 80

offset = -23

Line_pos = 580

delay = 60

detec = []
nuts = 0

def pega_centro(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

#url =('https://192.168.0.190:8080/video')
cap = cv2.VideoCapture('33.mp4')
subtracao = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    ret, frame1 = cap.read()
    tempo = float(1 / delay)
    sleep(tempo)
    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    frame1_sub = subtracao.apply(blur)
    dilat = cv2.dilate(frame1_sub, np.ones((5, 5)))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    ret, bin_img = cv2.threshold(dilatada, 250, 255, cv2.THRESH_BINARY_INV)
    canny= cv2.Canny(bin_img, 250, 255)
    #dilatada = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel)
    contours, h = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    cv2.line(frame1, (Line_pos, 100), (Line_pos, 350), (255, 255, 0), 5)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.02 * cv2.arcLength(cnt, True), True)
        cv2.drawContours(frame1, [approx], 0, (0, 0, 255), 2)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        x1, y1, w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        print(aspectRatio)




        if (aspectRatio) >= 0 and (aspectRatio) < 1.1:
            cv2.putText(frame1, "Cap", (x, y), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0))
        elif (aspectRatio) >= 1.25 and (aspectRatio) <= 1.35:
            cv2.putText(frame1, "Flange", (x, y), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0))
        elif (aspectRatio) >= 1.36:
            cv2.putText(frame1, "Wing", (x, y), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 0))

        (x, y, w, h) = cv2.boundingRect(cnt)
        validar_cnt = (w >= min_width) and (h >= Height_min)
        if not validar_cnt:
            continue

        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 255), 2)
        centro = pega_centro(x, y, w, h)
        detec.append(centro)
        cv2.circle(frame1, centro, 6, (255, 255, 255), 2)

        for (x, y) in detec:
            if x > (Line_pos + offset): #and x > (Line_pos - offset):
                nuts += 1
                #cv2.line(frame1, (Line_pos, 100), (Line_pos, 350), (0, 255, 255), 9)
                cv2.line(frame1, (Line_pos, 100), (Line_pos, 350), (255, 255, 0), 5)
                detec.remove((x, y))
                print("Nut is detected : " + str(nuts))

    cv2.putText(frame1, "Nut Detected :" + str(nuts), (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
    cv2.imshow("Video Original", frame1)
    cv2.imshow("Detectar", dilat)
    cv2.imshow("can", canny)
    cv2.imshow("bin", bin_img)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
cap.release()