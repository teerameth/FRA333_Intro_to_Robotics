import cv2, imutils
import numpy as np
from dijkstra import Graph, DijkstraSPF

def overlap(img_c, p1, p2):
    x0, y0 = min(p1[0], p2[0]), min(p1[1], p2[1])
    x1, y1 = max(p1[0], p2[0])+1, max(p1[1], p2[1])+1
    img_part = img_c[y0:y1, x0:x1]
    line_canvas = cv2.line(np.ones_like(img_part)*255, (p1[0]-x0, p1[1]-y0), (p2[0]-x0, p2[1]-y0), 0, 1)
    overlap = cv2.bitwise_or(img_part, line_canvas)
    if overlap.all() == 0: return True
    return False
def draw_path(img, points, path, zoom):
    divide = len(path)/160
    canvas_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for i in range(len(path)-1):
        a = points[path[i]]
        b = points[path[i+1]]
        cv2.line(canvas_hsv, (a[0]*zoom, a[1]*zoom), (b[0]*zoom, b[1]*zoom), (int(i/divide),255,255), 2)
    cv2.imshow("A", cv2.cvtColor(canvas_hsv, cv2.COLOR_HSV2BGR))
    cv2.waitKey(1)
img = cv2.imread('map/test_map2.png', 0)
map_size = img.shape
N = 1000
K = 10
start = (150, 200)
goal = (20, 20)

zoom = 3

c_space = 10
kernel = np.ones((c_space, c_space), dtype=np.uint8)
img_c = cv2.erode(img, kernel)

while True:
    canvas = cv2.cvtColor(imutils.resize(img, width=map_size[0]*zoom), cv2.COLOR_GRAY2BGR)
    cv2.circle(canvas, (start[0]*zoom, start[1]*zoom), 5, (0,0,255), -1)
    cv2.circle(canvas, (goal[0]*zoom, goal[1]*zoom), 5, (255,0,0), -1)

    points = [start, goal]
    while len(points) != N:
        x = np.random.randint(map_size[0])
        y = np.random.randint(map_size[1])
        if img_c[y][x] != 0: # not obstacle
            points.append((x, y))
            cv2.circle(canvas, (x*zoom, y*zoom), 3, (0, 255, 0), -1)
    cv2.imshow("A", canvas)
    cv2.waitKey(1)

    nodes = np.asarray(points)
    adj = np.zeros((N, N))
    for i in range(N):
        (x, y) = points[i]
        dist = np.sqrt(np.sum((nodes-nodes[i])**2, axis=1))
        indices = (dist).argsort()[:K]
        for j in indices:
            adj[i][j] = dist[j]
        for j in range(N):
            if adj[i][j] != 0 and i != j:
                if overlap(img_c, points[i], points[j]):
                    adj[i][j] = 0
                else:
                    cv2.line(canvas, (points[i][0]*zoom, points[i][1]*zoom), (points[j][0]*zoom, points[j][1]*zoom), (100,100,100), 1)
        if i%100 == 0:
            cv2.imshow("A", canvas)
            cv2.waitKey(1)
    cv2.waitKey(1)

    graph = Graph()
    for i in range(N):
        for j in range(N):
            if adj[i][j] != 0: graph.add_edge(i, j, adj[i][j])
    dijkstra = DijkstraSPF(graph, 0)
    path = dijkstra.get_path(1)
    draw_path(canvas.copy(), points, path, zoom)
    cv2.waitKey(1000)