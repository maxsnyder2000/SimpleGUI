try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

width = 400.0

n = 50
thres = 2

num_points = 80

center = (0, 0)
scale = 4.0

scale_times = 0.9

colors =["#FF0000",
         "#FF9900",
         "#FFFF00",
         "#00FF00",
         "#0000FF",
         "#9900FF",
         "#FF00FF"]

radius = width * 0.5/num_points

def set_points(s, with_center):
    p = []
    for i in range(num_points):
        for j in range(num_points):
            point = (s / num_points * i - s / 2,
                     s / num_points * j - s / 2)
            if with_center:
                point = (point[0] + center[0],
                         point[1] + center[1])
            p.append(point)
    return p

locs = set_points(width, False)
points = set_points(scale, True)

class Complex(object):
    def __init__(self, real, imag = 0.0):
        self.real = real
        self.imag = imag
    
    def __add__(self, other):
        return Complex(self.real + other.real,
                       self.imag + other.imag)
    
    def __mul__(self, other):
        return Complex(self.real*other.real - self.imag*other.imag,
                       self.imag*other.real + self.real*other.imag)

def mandel(c):
    a = Complex(0, 0)
    for i in range(n):
        a = a * a + c
        if -thres > a.real or a.real > thres or -thres > a.imag or a.imag > thres:
            return colors[i % len(colors)]
    return "Black"

def draw(canvas):
    for i in range(num_points * num_points):
        l = locs[i]
        p = points[i]
        c = Complex(p[0], p[1])
        canvas.draw_circle((l[0] + width / 2 + radius,
                            width / 2 - l[1] - radius),
                           radius, 0.5, "black", mandel(c))

def click(p):
    global scale, center, points
    scale *= scale_times
    center = (center[0] + (p[0] - width/2) * scale/width,
              center[1] + (width/2 - p[1]) * scale/width)
    points = set_points(scale, True)

frame = simplegui.create_frame("Mandelbrot Set", width, width)

frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)

frame.start()
