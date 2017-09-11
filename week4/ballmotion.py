# Ball motion with an explicit timer

import simpleguitk as simplegui

# Initialize globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
a = 0

ball_pos = [WIDTH / 2, HEIGHT / 2]
vel = [1, 1]  # pixels per tick

def keydown(key):
    global a
    if key == simplegui.KEY_MAP["right"] or key == simplegui.KEY_MAP["d"]:
       a += 1
    elif key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["a"]:
       a -= 1


def draw(canvas):
    # calculate ball position
    if ball_pos[0] >= WIDTH - 1 - BALL_RADIUS:
        vel[0] = vel[0] * -1
    elif ball_pos[0] <= BALL_RADIUS:
        vel[0] = vel[0] * -1
    elif ball_pos[1] >= HEIGHT + 1 - BALL_RADIUS:
        vel[1] = vel[1] * -1
    elif ball_pos[1] <= BALL_RADIUS:
        vel[1] = vel[1] * -1

    ball_pos[0] += vel[0]
    ball_pos[1] += vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

# create frame
frame = simplegui.create_frame("Motion", WIDTH, HEIGHT)

# register event handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)

# start frame
frame.start()