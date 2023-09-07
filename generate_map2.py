import cv2
import numpy as np
import imutils

img = np.ones((300, 300), dtype=np.uint8)*255
img = cv2.fillPoly(img, [np.array([[20,40],[60,140],[140,80],[80,20]], dtype=np.int32)], 0)
cv2.circle(img, (150, 150), 40, 0, -1)
cv2.rectangle(img, (160, 160), (250, 250), 0, thickness=-1)
# cv2.rectangle(img, (120, 150), (140, 300), 0, thickness=-1)
cv2.rectangle(img, (200, 0), (220, 150), 0, thickness=-1)

cv2.imshow("A", img)
cv2.waitKey(0)
cv2.imwrite("map/test_map2.png", img)
for x in range(0, 311, 10):
    cv2.line(img, (0, x), (300, x), 50, 1)
for y in range(0, 311, 10):
    cv2.line(img, (y, 0), (y, 300), 50, 1)
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
cv2.circle(img, (150, 200), 5, (0, 0, 255), -1) # start
cv2.circle(img, (20, 20), 5, (255, 0, 0), -1) # goal
cv2.imshow("A", img)
cv2.waitKey(0)
cv2.imwrite("map/test_map_grid2.png", img)