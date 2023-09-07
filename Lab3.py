import math
def euclidean(p1, p2): return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
names = ['1A', '2A', '4A', '6A', '1B', '2B', '4C', '6C', '1E', '3E', '5D', '6D', '1F', '3F','5F','6F']
pos = {'1A':(10,150), '2A':(40,150), '4A':(100,150), '6A':(150,150), '1B':(10,90), '2B':(100/3,320/3), '4C':(340,120),'6C':(150,110), '1E':(10,30), '3E':(80/3,40), '5D':(120,40), '6D':(150,50), '1F':(10,10), '3F':(50,10), '5F':(110,10), '6F':(150,10)}
adj = [[0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [1,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0],
        [0,1,0,1,0,0,1,0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0],
        [1,0,0,0,0,1,0,0,1,0,1,0,0,0,0,0],
        [0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0],
        [0,0,0,1,0,0,1,0,0,0,0,1,0,0,0,0],
        [0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0],
        [0,0,0,0,1,0,0,0,0,0,0,1,0,0,1,0],
        [0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1],
        [0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,0,1,0,0,1,0,1,0],
        [0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,1],
        [0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0]]
def avaliable_node(picked):
    nodes = []
    for i in range(len(names)):
        if adj[picked[-1]][i] == 1 and i!=picked[-1] and i not in picked: nodes.append(i)
    return nodes
start, goal = 13, 3 # "3F", "6A"
def search(picked):
    this_node = picked[-1]
    if this_node == goal:
        [print(names[pick], end='-') for pick in picked]
        print(sum([euclidean(pos[names[picked[i]]], pos[names[picked[i+1]]]) for i in range(len(picked)-1)]))
        return
    nodes = avaliable_node(picked)
    if len(nodes) == 0: return
    for node in nodes:
        search(picked+[node])
picked = [start]
search(picked)

for i in range(len(names)):
    for j in range(i):
        if adj[i][j] == 1:
            # print("%s - %s"%(names[j], names[i]))
            # print("\'%s\'"%names[i], end=' ')
            print("%d" % (i+1), end=' ')