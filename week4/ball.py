# control the position of a ball using the arrow keys

import simpleguitk as simplegui

# Initialize globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20

ball_pos = [WIDTH / 2, HEIGHT / 2]

# define event handlers
def draw(canvas):
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

def keydown(key):
    vel = 4
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["a"]:
        ball_pos[0] -= vel
    elif key == simplegui.KEY_MAP["right"] or key == simplegui.KEY_MAP["d"]:
        ball_pos[0] += vel
    elif key == simplegui.KEY_MAP["down"] or key == simplegui.KEY_MAP["s"]:
        ball_pos[1] += vel
    elif key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["w"]:
        ball_pos[1] -= vel

    # create frame
frame = simplegui.create_frame("Positional ball control", WIDTH, HEIGHT)

# register event handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)

# start frame
frame.start()
