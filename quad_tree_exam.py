import cv2, imutils
import numpy as np
img = np.ones((160, 160), dtype=np.uint8)*255
img = cv2.fillPoly(img, [np.array([[-20+80,60+80],[-60+80,0+80],[20+80,10+80]], dtype=np.int32)], 0)
img = cv2.fillPoly(img, [np.array([[-20+80,-40+80],[0+80,-60+80],[50+80,-60+80],[50+80,-20+80]], dtype=np.int32)], 0)
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
    points1 = [(rect1.x, rect1.y), (rect1.x, y1), (x1, rect1.y), (x1, y1)]
    points2 = [(rect2.x, rect2.y), (rect2.x, y2), (x2, rect2.y), (x2, y2)]
    for point in points1:
        if point in points2: return True
    return vertical_shared or horizontal_shared
class QuadTree():
    def __init__(self, min_size, img, zoom=3):
        self.min_size = min_size
        self.zoom = zoom
        self.original_shape = img.shape
        self.new_size = img.shape[0]
        self.img = cv2.dilate(img, np.ones((3,3))) # dilate นึดนึงเพื่อป้องกันการเกยของมุมภาพสิ่งกีดขวาง
        self.canvas = cv2.cvtColor(imutils.resize(self.img, width = img.shape[0]*zoom), cv2.COLOR_GRAY2BGR)
        for x in range(0, self.canvas.shape[0], 10*zoom):
            cv2.line(self.canvas, (0, x), (self.canvas.shape[1], x), (100,100,100), 1)
        for y in range(0, self.canvas.shape[1], 10*zoom):
            cv2.line(self.canvas, (y, 0), (y, self.canvas.shape[0]), (100,100,100), 1)
        self.leave = []
        self.root = Node(0, 0, self.new_size)
        self.recursive(self.root)
        cv2.imshow("Preview", cv2.flip(self.canvas, 0))
        cv2.imwrite("grid.jpg", cv2.flip(self.canvas, 0))
        cv2.waitKey(1000)
        for i in range(len(self.leave)):
            for j in range(len(self.leave)):
                if i != j and shared_edge(self.leave[i], self.leave[j]):
                    self.leave[i].neighbor.append(j)
                    x1 = (self.leave[i].x+int(self.leave[i].size/2))*self.zoom
                    y1 = (self.leave[i].y+int(self.leave[i].size/2))*self.zoom
                    x2 = (self.leave[j].x + int(self.leave[j].size / 2)) * self.zoom
                    y2 = (self.leave[j].y + int(self.leave[j].size / 2)) * self.zoom
                    cv2.line(self.canvas, (x1, y1), (x2, y2), (250, 206, 135), 2)
                    # cv2.imshow("Preview", self.canvas)
                    # cv2.waitKey(1)

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
                              (150, 0, 150), 2)
            # cv2.imshow("Preview", self.canvas)
            # cv2.waitKey(1)

Q = QuadTree(20, img) # limit size at 20x20 cm.
cv2.imshow("Preview", cv2.flip(Q.canvas, 0))
cv2.imwrite("edge.jpg", cv2.flip(Q.canvas, 0))
cv2.waitKey(1000)

import math
def euclidean(p1, p2): return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

names = ['b13','c16','c17','c15','b9','c9','c7','c8','c18','c19','c21','c22','c20','c10','c11', 'c14', 'c12','c13','c4','c3','b1','c1','c2','c6','c5','b8','b3','b4']
print(len(names))
pos = {}

for i in range(len(Q.leave)):
    pos[names[i]] = (Q.leave[i].x+Q.leave[i].size/2, Q.leave[i].y+Q.leave[i].size/2)
for i in range(len(Q.leave)):
    print(int(pos[names[i]][0]-80), end = " ")
print('\n')
for i in range(len(Q.leave)):
    print(int(pos[names[i]][1]-80), end = " ")

adj = np.zeros((len(Q.leave), len(Q.leave)), dtype=np.uint8)
all_path = []
Q.canvas = cv2.flip(Q.canvas, 0)
for i in range(len(Q.leave)):
    (x1, y1) = (Q.leave[i].x+Q.leave[i].size/2, Q.leave[i].y+Q.leave[i].size/2)
    for j in range(len(Q.leave[i].neighbor)):
        index = Q.leave[i].neighbor[j]
        adj[i][index] = 1
        neighbor = Q.leave[Q.leave[i].neighbor[j]]
        (x2, y2) = (neighbor.x+neighbor.size/2, neighbor.y+neighbor.size/2)
    cv2.putText(Q.canvas, names[i], (int(x1)*Q.zoom, Q.canvas.shape[1] - int(y1)*Q.zoom), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_AA)
    cv2.putText(Q.canvas, str((int(x1-80),int(y1-80))), (int(x1) * Q.zoom-20, Q.canvas.shape[1] - int(y1) * Q.zoom-20), cv2.FONT_HERSHEY_SIMPLEX,0.3, (255, 0, 0), 1, cv2.LINE_AA)
    # cv2.putText(Q.canvas, str(i), (int(x1) * Q.zoom, Q.canvas.shape[1] - int(y1) * Q.zoom), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
cv2.imshow("Preview", Q.canvas)
cv2.waitKey(1000)
print(adj)
for i in range(len(adj)):
    for j in range(len(adj)):
        if adj[i][j] != 0:
            print(i+1, end=" ")
print("\n")
for i in range(len(adj)):
    for j in range(len(adj)):
        if adj[i][j] != 0:
            print(j+1, end=" ")
print("\n")

def avaliable_node(picked):
    nodes = []
    for i in range(len(names)):
        if adj[picked[-1]][i] == 1 and i!=picked[-1] and i not in picked: nodes.append(i)
    return nodes
start, goal = names.index('b13'), names.index('b3') # "3F", "6A"
best = {'cost':None, 'path':None}
def search(picked):
    global best
    this_node = picked[-1]
    if this_node == goal:
        # [print(names[pick], end='-') for pick in picked]
        cost = sum([euclidean(pos[names[picked[i]]], pos[names[picked[i+1]]]) for i in range(len(picked)-1)])
        if best['cost'] == None:
            best['cost'] = cost
            best['path'] = [names[pick] for pick in picked]
        if best['cost'] > cost:
            best['cost'] = cost
            best['path'] = [names[pick] for pick in picked]
        return
    nodes = avaliable_node(picked)
    if len(nodes) == 0: return
    for node in nodes:
        search(picked+[node])
picked = [start]
search(picked)
print(best)
Q.canvas = cv2.flip(Q.canvas, 0)
for i in range(len(best['path'])-1):
    a = Q.leave[names.index(best['path'][i])]
    b = Q.leave[names.index(best['path'][i+1])]
    x1 = (a.x + int(a.size / 2)) * Q.zoom
    y1 = (a.y + int(a.size / 2)) * Q.zoom
    x2 = (b.x + int(b.size / 2)) * Q.zoom
    y2 = (b.y + int(b.size / 2)) * Q.zoom
    cv2.line(Q.canvas, (x1, y1), (x2, y2), (0,0,255), 2)
Q.canvas = cv2.flip(Q.canvas, 0)
cv2.imshow("Preview", Q.canvas)
cv2.waitKey(0)