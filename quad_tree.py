import cv2, imutils
import numpy as np

class Node():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.children = []
        self.neighbor = []
    def img(self, image):
        return image[self.y:self.y+self.size, self.x:self.x+self.size]
def shared_edge(rect1, rect2):
    x1, y1 = rect1.x + rect1.size, rect1.y + rect1.size
    x2, y2 = rect2.x + rect2.size, rect2.y + rect2.size
    horizontal_shared = (y1 == rect2.y or y2 == rect1.y) and x1 > rect2.x and x2 > rect1.x
    vertical_shared = (x1 == rect2.x or x2 == rect1.x) and y1 > rect2.y and y2 > rect1.y
    return vertical_shared or horizontal_shared
class QuadTree():
    def __init__(self, min_size, img, zoom=3):
        self.min_size = min_size
        self.zoom = zoom
        self.original_shape = img.shape
        # zero padding
        i = 1
        while 2**i < max(img.shape): i += 1
        self.new_size = 2**i
        self.img = np.zeros((self.new_size, self.new_size)) # create empty image
        self.img[0:self.original_shape[1], 0:self.original_shape[0]] = img
        self.canvas = cv2.cvtColor(imutils.resize(img, width = img.shape[0]*zoom), cv2.COLOR_GRAY2BGR)
        self.leave = []
        self.root = Node(0, 0, self.new_size)
        self.recursive(self.root)
        for i in range(len(self.leave)):
            for j in range(len(self.leave)):
                if i != j and shared_edge(self.leave[i], self.leave[j]):
                    self.leave[i].neighbor.append(j)
                    x1 = (self.leave[i].x+int(self.leave[i].size/2))*self.zoom
                    y1 = (self.leave[i].y+int(self.leave[i].size/2))*self.zoom
                    x2 = (self.leave[j].x + int(self.leave[j].size / 2)) * self.zoom
                    y2 = (self.leave[j].y + int(self.leave[j].size / 2)) * self.zoom
                    cv2.line(self.canvas, (x1, y1), (x2, y2), (250, 206, 135), 1)
                    cv2.imshow("Preview", self.canvas)
                    cv2.waitKey(1)

    def recursive(self, node):
        image = node.img(self.img)
        contain = np.unique(image.reshape(-1), axis=0)
        if len(contain) > 1 and node.size>self.min_size:
            if node.size > self.min_size and node.size > self.min_size: # divide to quad
                half = int(node.size/2)
                node.children.append(Node(node.x, node.y, half))
                node.children.append(Node(node.x + half, node.y, half))
                node.children.append(Node(node.x, node.y + half, half))
                node.children.append(Node(node.x + half, node.y + half, half))
                for child in node.children: self.recursive(child)
        else: # is leaf node
            if contain[0] == 0 or len(contain) > 1:
                cv2.rectangle(self.canvas, (node.x * self.zoom, node.y * self.zoom),
                              ((node.x + node.size) * self.zoom,(node.y + node.size) * self.zoom),
                              (0, 0, 0), -1)
            else:
                self.leave.append(node)
                cv2.rectangle(self.canvas, (node.x * self.zoom, node.y * self.zoom),
                              ((node.x + node.size) * self.zoom, (node.y + node.size) * self.zoom),
                              (150, 150, 150), 1)
            cv2.imshow("Preview", self.canvas)
            cv2.waitKey(1)

img = cv2.imread('map/test_map2.png', 0)
Q = QuadTree(2, img)
print(len(Q.leave))
L = []
for l in Q.leave:
    L.append(l.size)
(unique, count) = np.unique(L, return_counts=True)
for i in range(len(unique)):
    print("%d: %d"%(unique[i], count[i]))
cv2.imshow("Preview", Q.canvas)
cv2.waitKey(0)