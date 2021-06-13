try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random

W = 1000
H = 100 # or 10

color_list = ["Red", "Yellow", "Blue", "Green"]

# ENDS
END_LENGTH = W / 10
COLOR_LENGTH = W / (len(color_list) * 4)

# COLORS
colors = []
def randomize_colors():
    global color_list, colors
    random.shuffle(color_list)
    colors = []
    i = END_LENGTH
    j = W - END_LENGTH
    for color in color_list:
        colors.append([i, i + COLOR_LENGTH, j - COLOR_LENGTH, j, color])
        i += COLOR_LENGTH
        j -= COLOR_LENGTH
randomize_colors()

# SCORES
MAX_SCORE = 10
score_1 = 0.0
score_2 = 0.0

# PLAYERS
P_SIZE = W / 20
p_1 = W / 4
p_2 = W - p_1

PVEL = W / 500.0
v_1 = 0
v_2 = 0

# BALL
RAD = 10
ball = W / 2

BVEL = W / 400.0
bv = 0
ball_color = "White"
point_decided = False

def new_ball():
    global bv, ball_color, point_decided
    bv = BVEL * random.choice([-1, 1])
    ball_color = random.choice(color_list)
    point_decided = False
    randomize_colors()
new_ball()

def draw(canvas):
    # ENDS
    canvas.draw_line((0, H / 2), (END_LENGTH, H / 2), H, "White")
    canvas.draw_line((W - END_LENGTH, H / 2), (W, H / 2), H, "White")
    
    # COLORS
    for col in colors:
        canvas.draw_line((col[0], H / 2), (col[1], H / 2), H, col[4])
        canvas.draw_line((col[2], H / 2), (col[3], H / 2), H, col[4])
    
    # SCORES
    global score_1, score_2, won
    end_score_1 = END_LENGTH * (score_1 / MAX_SCORE)
    end_score_2 = W - END_LENGTH * (score_2 / MAX_SCORE)
    score_height = 40
    
    if score_1 >= MAX_SCORE:
        end_score_1 = W
        score_height = H
    if score_2 >= MAX_SCORE:
        end_score_2 = 0
        score_height = H
    
    if score_2 < MAX_SCORE:
        canvas.draw_line((0, H / 2), (end_score_1, H / 2), score_height, "Pink")
    if score_1 < MAX_SCORE:
        canvas.draw_line((end_score_2, H / 2), (W, H / 2), score_height, "Purple")
    
    if score_1 < MAX_SCORE and score_2 < MAX_SCORE:
        # PLAYERS
        global p_1, p_2
        color_1 = "White"
        color_2 = "White"
        for col in colors:
            if p_1 >= col[0] and p_1 <= col[1]:
                color_1 = col[4]
            if p_2 >= col[2] and p_2 <= col[3]:
                color_2 = col[4]
        
        p_1 += v_1
        if p_1 <= colors[0][0] + P_SIZE / 2:
            p_1 = colors[0][0] + P_SIZE / 2
        if p_1 >= colors[len(color_list) - 1][1] - P_SIZE / 2:
            p_1 = colors[len(color_list) - 1][1] - P_SIZE / 2
        
        p_2 += v_2
        if p_2 >= colors[0][3] - P_SIZE / 2:
            p_2 = colors[0][3] - P_SIZE / 2
        if p_2 <= colors[len(color_list) - 1][2] + P_SIZE / 2:
            p_2 = colors[len(color_list) - 1][2] + P_SIZE / 2
        
        canvas.draw_polygon([(p_1 - P_SIZE / 2, H / 2 + P_SIZE / 4),
                             (p_1 - P_SIZE / 2, H / 2 - P_SIZE / 4),
                             (p_1 + P_SIZE / 2, H / 2 - P_SIZE / 4),
                             (p_1 + P_SIZE / 2, H / 2 + P_SIZE / 4)], 5, "Black", color_1)
        canvas.draw_polygon([(p_2 - P_SIZE / 2, H / 2 + P_SIZE / 4),
                             (p_2 - P_SIZE / 2, H / 2 - P_SIZE / 4),
                             (p_2 + P_SIZE / 2, H / 2 - P_SIZE / 4),
                             (p_2 + P_SIZE / 2, H / 2 + P_SIZE / 4)], 5, "Black", color_2)
        
        # BALL
        global ball, bv, ball_color, point_decided
        ball += bv
        canvas.draw_circle((ball, H / 2), RAD, 5, "Grey", ball_color)
        
        # bounces
        if not point_decided:
            if ball <= p_1 + P_SIZE / 2 + RAD:
                if color_1 == ball_color:
                    bv *= -1.1
                    ball_color = random.choice(color_list)
                    randomize_colors()
                else:
                    point_decided = True
            if ball >= p_2 - P_SIZE / 2 - RAD:
                if color_2 == ball_color:
                    bv *= -1.1
                    ball_color = random.choice(color_list)
                    randomize_colors()
                else:
                    point_decided = True
        
        # points
        if ball < RAD:
            score_2 += 1
            ball = W / 2
            new_ball()
        if ball > W - RAD:
            score_1 += 1
            ball = W / 2
            new_ball()

def keyup(key):
    global v_1, v_2
    if key == simplegui.KEY_MAP["A"]:
        v_1 = 0
    if key == simplegui.KEY_MAP["D"]:
        v_1 = 0
    if key == simplegui.KEY_MAP["left"]:
        v_2 = 0
    if key == simplegui.KEY_MAP["right"]:
        v_2 = 0

def keydown(key):
    global v_1, v_2
    if key == simplegui.KEY_MAP["A"]:
        v_1 = -PVEL
    if key == simplegui.KEY_MAP["D"]:
        v_1 = PVEL
    if key == simplegui.KEY_MAP["left"]:
        v_2 = -PVEL
    if key == simplegui.KEY_MAP["right"]:
        v_2 = PVEL

frame = simplegui.create_frame("1D Game", W, H)

frame.set_draw_handler(draw)
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)

frame.start()
