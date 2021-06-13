try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math

FN = "The Nick Cavanaugh Volume Knob"
FW = 250.0
FH = 250.0
FO = (FW / 2, FH / 2)
FC = "White"

KR = FW / 5
KC = "Black"
KLW = 5
KLC = "Gray"

BR1 = KR + 4
BR2 = 5
BC = "Red"
BLW = 1
BLC = "Yellow"

DELTA = 0.0001

LINEAR = 0.05
PRE_LINEAR = 10
POST_LINEAR = 0.5

SAMP = 2
SENS = 0.05

click = (FW / 2, FH / 2 - BR1)
curr_frame = 0
last_click = None

is_dragging = False

ML = "https://a.tmp.ninja/iYpoHNM.mp3"

L_PLAY = "Play"
L_PAUSE = "Pause"
L_REWIND = "Restart"
L_VOLUME = "Volume: "

is_playing = False

volume = 0.5
VOLUME_MAX = 100

def neg(v):
    return (-v[0], -v[1])

def add(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

def sub(v1, v2):
    return add(v1, neg(v2))

def mult(v, s):
    return (v[0] * s, v[1] * s)

def div(v, s):
    return mult(v, 1.0 / (s + DELTA))

def norm(v):
    mag = (v[0] ** 2 + v[1] ** 2) ** 0.5
    return div(v, mag)

def rad(v):
    return math.atan2(v[1], v[0])

def rad_diff(r1, r2):
    diff = r1 - r2
    if abs(diff) < math.pi:
        return diff
    elif diff >= math.pi:
        return diff - math.pi * 2
    else:
        return diff + math.pi * 2

def f(x):
    if x < -LINEAR:
        return x * PRE_LINEAR
    elif x < LINEAR:
        return x
    else:
        return x * POST_LINEAR

def draw(canvas):
    global curr_frame
    canvas.draw_circle(FO, KR, KLW, KLC, KC)
    if is_dragging:
        canvas.draw_circle(click, BR2, BLW, BLC, BC)
    curr_frame += 1

def drag(coord):
    global is_dragging, curr_frame, last_click, click
    curr_click = norm(sub(coord, FO))
    is_dragging = True
    if curr_frame > SAMP:
        if last_click != None:
            prev = rad(last_click)
            curr = rad(curr_click)
            diff = f(rad_diff(curr, prev) * SENS)
            set_volume(max(0, min(1, volume + diff)))
        curr_frame = 0
        last_click = curr_click
    click = add(FO, mult(curr_click, BR1))

def click(coord):
    global last_click, is_dragging
    last_click = None
    is_dragging = False

frame = simplegui.create_frame(FN, FW, FH)
frame.set_canvas_background(FC)

frame.set_draw_handler(draw)
frame.set_mousedrag_handler(drag)
frame.set_mouseclick_handler(click)

sound = simplegui.load_sound(ML)

def play_pause():
    global is_playing
    is_playing = not is_playing
    if is_playing:
        sound.play()
        button1.set_text(L_PAUSE)
    else:
        sound.pause()
        button1.set_text(L_PLAY)

def rewind():
    sound.rewind()
    if is_playing:
        sound.play()

button1 = frame.add_button(L_PLAY, play_pause)
button2 = frame.add_button(L_REWIND, rewind)

label = frame.add_label(L_VOLUME)

def set_volume(v):
    global volume
    volume = v
    sound.set_volume(v)
    label.set_text(L_VOLUME + str(int(v * VOLUME_MAX)) + " / " + str(VOLUME_MAX))
set_volume(volume)

frame.start()
