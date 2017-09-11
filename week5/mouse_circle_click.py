# Examples of mouse input

import simpleguitk as simplegui
import math

# intialize globals
WIDTH = 450
HEIGHT = 300
ball_pos_list = []
BALL_RADIUS = 15


# helper function - pytagoras
def distance(p, q):
    """
    The distance between two point
    :param p: first coordinate: tuple of x an y coordinates
    :param q: second coordinate: tuple of x an y coordinates
    :return: the distance between the two pints
    """
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# define event handler for mouse click, draw
def click(pos):
    changed = False

    for ball_pos in ball_pos_list:
        if distance([pos[0], pos[1]], ball_pos) < BALL_RADIUS:
            if ball_pos[2] == "Green":
                ball_pos[2] = "Red"
            else:
                ball_pos[2] = "Green"
            changed = True

    if changed == False:
        ball_pos_list.append([pos[0], pos[1], "Red"])


def draw(canvas):
    for pos in ball_pos_list:
        canvas.draw_circle([pos[0], pos[1]], BALL_RADIUS, 1, "Black", pos[2])

# create frame
frame = simplegui.create_frame("Mouse selection", WIDTH, HEIGHT)
frame.set_canvas_background("White")

# register event handler
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

# start frame
frame.start()