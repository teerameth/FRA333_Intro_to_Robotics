import cv2
import numpy as np
import imutils

img = np.ones((300, 300), dtype=np.uint8)*255
img = cv2.fillPoly(img, [np.array([[20,40],[60,140],[140,80],[80,20]], dtype=np.int32)], 0)
cv2.circle(img, (150, 150), 40, 0, -1)
cv2.rectangle(img, (160, 160), (250, 250), 0, thickness=-1)

cv2.imshow("A", img)
cv2.waitKey(0)
cv2.imwrite("map/test_map.png", img)
for x in range(0, 311, 10):
    cv2.line(img, (0, x), (300, x), 50, 1)
for y in range(0, 311, 10):
    cv2.line(img, (y, 0), (y, 300), 50, 1)
cv2.imshow("A", img)
cv2.waitKey(0)
cv2.imwrite("map/test_map_grid.png", img)