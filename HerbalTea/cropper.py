import cv2
img = cv2.imread("house_map.pgm")
x,y,w,h = 240, 70, 125, 125
crop_img = img[y:y+h, x:x+w]
cv2.imshow("cropped", crop_img)
cv2.waitKey(0)
