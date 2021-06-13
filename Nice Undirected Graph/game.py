try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random

groups = {}

groups["Bruford"] = ("Bill Bruford", "Allan Holdsworth", "Dave Stewart")
groups["Egg"] = ("Clive Brooks", "Mont Campbell", "Dave Stewart")
groups["Enigmatic Ocean"] = ("Allan Holdsworth", "Jean-Luc Ponty")
groups["Gong"] = ("Steve Hillage", "Pip Pyle")
groups["Hatfield and the North"] = ("Phil Miller", "Pip Pyle", "Richard Sinclair", "Dave Stewart")
groups["Khan"] = ("Steve Hillage", "Dave Stewart")
groups["King Crimson"] = ("Bill Bruford", "Robert Fripp", "John Wetton")
groups["UK 1"] = ("Bill Bruford", "Allan Holdsworth", "Eddie Jobson", "John Wetton")
groups["UK 2"] = ("Terry Bozzio", "Eddie Jobson", "John Wetton")
groups["Uriel"] = ("Clive Brooks", "Mont Campbell", "Steve Hillage", "Dave Stewart")
groups["Zappa 1973"] = ("George Duke", "Jean-Luc Ponty", "Frank Zappa")
groups["Zappa 1976"] = ("Terry Bozzio", "Eddie Jobson", "Frank Zappa")

NAME = "\"Nice\" Undirected Graph"
W = 500.0
H = 500.0
B = (W + H) / 50
R = (W * H) ** 0.5 / 50

DELTA = 0.0001

WE = 5
CE0 = "White"
CE1 = "Green"
CE2 = "Yellow"

WN = 2
CN0 = "White"
CN1 = "Red"
CN2 = "Blue"
CNB = "Gray"

FE = -0.01
FN = 0.001
FG = -0.001
FF = 0.25
F_MAX = 10000

WL = 200

STEPS = 1
TOTAL = None

class Graph:
    def __init__(self, groups):
        graph = {}
        nodes = set()
        for group in groups:
            for n1 in groups[group]:
                if n1 not in graph:
                    graph[n1] = {}
                for n2 in groups[group]:
                    if n1 != n2:
                        if n2 not in graph[n1]:
                            graph[n1][n2] = [group]
                        else:
                            graph[n1][n2].append(group)
                nodes.add(n1)
        for n1 in nodes:
            for n2 in nodes:
                if n2 not in graph[n1]:
                    graph[n1][n2] = None
        self.graph = graph
        self.nodes = sorted(nodes)

graph = Graph(groups)

def add(c1, c2):
    return (c1[0] + c2[0], c1[1] + c2[1])

def clamp(low, n, high):
    return max(low, min(high, n))

def dist(c1, c2):
    return ((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2) ** 0.5

def direction(c1, c2):
    d = dist(c1, c2)
    if d < DELTA:
        return (random.random(), random.random())
    else:
        return ((c1[0] - c2[0]) / d, (c1[1] - c2[1]) / d)

def force(c1, c2, mag):
    d = direction(c1, c2)
    return (d[0] * mag, d[1] * mag)

def force_edges(curr, n1, n2):
    c1 = curr[n1]
    c2 = curr[n2]
    return force(c1, c2, FE * dist(c1, c2))

def force_nodes(curr, n1, n2):
    c1 = curr[n1]
    c2 = curr[n2]
    return force(c1, c2, FN / (dist(c1, c2) ** 2 + DELTA))

def force_gravity(c):
    c1 = c
    c2 = (0.5, 0.5)
    return force(c1, c2, FG * dist(c1, c2))

def coords_random():
    coords = {}
    for node in graph.nodes:
        coords[node] = (random.random(), random.random(), 0, 0)
    return coords

def coords_reset():
    global coords
    set_node_1(None)
    coords = coords_random()

coords = coords_random()
step = 0

def coords_step(curr):
    coords = dict(curr)
    for n1 in graph.nodes:
        coord = coords[n1]
        f = (0, 0)
        for n2 in graph.nodes:
            if n1 == n2:
                continue
            if graph.graph[n1][n2] != None:
                fe = force_edges(curr, n1, n2)
                f = add(f, fe)
            fn = force_nodes(curr, n1, n2)
            f = add(f, fn)
        fg = force_gravity(coord)
        f = add(f, fg)
        f = (clamp(-F_MAX, f[0], F_MAX),
             clamp(-F_MAX, f[1], F_MAX))
        v = ((f[0] + coord[2]) * (1 - FF),
             (f[1] + coord[3]) * (1 - FF))
        coord = (coord[0] + v[0],
                 coord[1] + v[1],
                 v[0],
                 v[1])
        coords[n1] = coord
    return coords

sel_node_1 = None
sel_node_2 = None
sel_edge = None

def set_node_1(node):
    global sel_node_1, sel_node_2, sel_edge
    sel_node_1 = node
    sel_node_2 = None
    sel_edge = None
    set_label()

def set_node_2(node):
    global sel_node_2, sel_edge
    sel_node_2 = node
    if node == None:
        sel_edge = None
    else:
        sel_edge = graph.graph[sel_node_1][sel_node_2][0]
    set_label()

frame = simplegui.create_frame(NAME, W, H)

def glob(coords, idx):
    x_min = min([coords[coord][0] for coord in coords])
    x_max = max([coords[coord][0] for coord in coords])
    y_min = min([coords[coord][1] for coord in coords])
    y_max = max([coords[coord][1] for coord in coords])
    x_norm = (coords[idx][0] - x_min) / (x_max - x_min)
    y_norm = (coords[idx][1] - y_min) / (y_max - y_min)
    return (B + x_norm * (W - B * 2),
            B + y_norm * (H - B * 2))

def draw(canvas):
    global step, coords
    if step != TOTAL:
        step += 1
        if step % STEPS == 0:
            coords = coords_step(coords)
    for n1 in graph.nodes:
        for n2 in graph.nodes:
            if graph.graph[n1][n2] == None:
                continue
            c1 = glob(coords, n1)
            c2 = glob(coords, n2)
            color = CE0
            if sel_edge in graph.graph[n1][n2]:
                color = CE1
            if set([n1, n2]) == set([sel_node_1, sel_node_2]):
                color = CE2
            canvas.draw_line(c1, c2, WE, color)
    for name in coords:
        color = CN0
        if name == sel_node_1:
            color = CN1
        elif name == sel_node_2:
            color = CN2
        canvas.draw_circle(glob(coords, name), R, WN, CNB, color)

frame.set_draw_handler(draw)

def min_name(coord, other):
    min_name = None
    min_dist = W + H
    for name in coords:
        curr_dist = dist(coord, glob(coords, name))
        if other == None or graph.graph[name][other] != None or name == other:
            if curr_dist < min_dist:
                min_name = name
                min_dist = curr_dist
    return min_name if min_name != other else None

def drag(coord):
    if sel_node_1 == None:
        set_node_1(min_name(coord, None))
    else:
        set_node_2(min_name(coord, sel_node_1))

frame.set_mousedrag_handler(drag)

def click(coord):
    set_node_1(None)

frame.set_mouseclick_handler(click)

button = frame.add_button("RESET", coords_reset)

label_1 = frame.add_label("", WL)
label_2 = frame.add_label("", WL)
label_3 = frame.add_label("", WL)
label_4 = frame.add_label("", WL)

def set_label():
    if sel_node_1 == None:
        label_1.set_text("")
    else:
        label_1.set_text(CN1.upper() + ": " + sel_node_1)
    if sel_node_2 == None:
        label_2.set_text("")
    else:
        label_2.set_text(CN2.upper() + ": " + sel_node_2)
    if sel_edge == None:
        label_3.set_text("")
        label_4.set_text("")
    else:
        label_3.set_text(CE1.upper() + ": " + sel_edge)
        label_4.set_text(CE2.upper() + ": " + ", ".join(graph.graph[sel_node_1][sel_node_2]))

frame.start()
