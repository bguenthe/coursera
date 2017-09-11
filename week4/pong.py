# Implementation of classic arcade game Pong

import simpleguitk as simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

ball_pos = [0, 0]
ball_vel = [1, 1]
ball_acc = 0.0
paddleleft_pos = 0
paddleright_pos = 0
paddleleft_vel = 0
paddle_acc = 6
paddleright_vel = 0
scoreleft = 0
scoreright = 0
paddleright_direction = ""
paddleleft_direction = ""


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel  # these are vectors stored as lists

    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == 1:
        ball_vel[0] = (random.randrange(120, 240) / 60)
        ball_vel[1] = (random.randrange(60, 180) / 60) * random.randrange(-1, 2, 2)
    else:
        ball_vel[0] = (random.randrange(120, 240) / 60) * -1
        ball_vel[1] = (random.randrange(60, 180) / 60) * random.randrange(-1, 2, 2)

def reset_handler():
    new_game(0)


# define event handlers
def new_game(direction):
    global paddleleft_pos, paddleright_pos, paddleleft_vel, paddleright_vel  # these are numbers
    global scoreleft, scoreright, ball_acc

    paddleleft_pos = HEIGHT / 2
    paddleright_pos = HEIGHT / 2
    paddleleft_vel = 0
    paddleright_vel = 0

    ball_acc = 1.0
    if direction == 0:
        scoreleft = 0
        scoreright = 0
        ran = random.randrange(1, 3)
        print ran
        if ran == 1:
            spawn_ball(1)
        else:
            spawn_ball(-1)
    elif direction == 1:
        scoreleft += 1
        spawn_ball(-1)
    else:
        scoreright += 1
        spawn_ball(1)


def draw(canvas):
    global soreleft, scoreright, paddleleft_pos, paddleright_pos, ball_pos, ball_vel
    global paddleright_direction, paddleleft_direction, ball_acc

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    if ball_vel[0] > 0:
        ball_pos[0] += ball_vel[0] + ball_acc
    else:
        ball_pos[0] += ball_vel[0] - ball_acc

    if ball_vel[1] > 0:
        ball_pos[1] += ball_vel[1] + ball_acc
    else:
        ball_pos[1] += ball_vel[1] - ball_acc

    # abprallen, wenn auf paddle; and der rechten wand und im paddle bereich
    if ball_pos[0] >= (WIDTH - 1 - BALL_RADIUS - PAD_WIDTH):
        if (ball_pos[1] + BALL_RADIUS >= paddleright_pos - HALF_PAD_HEIGHT) and (
                        ball_pos[1] + BALL_RADIUS <= paddleright_pos + HALF_PAD_HEIGHT):
            ball_vel[0] = ball_vel[0] * -1
            ball_acc += 0.3
        else:
            new_game(1)
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if (ball_pos[1] + BALL_RADIUS >= paddleleft_pos - HALF_PAD_HEIGHT) and (
                        ball_pos[1] + BALL_RADIUS <= paddleleft_pos + HALF_PAD_HEIGHT):
            ball_vel[0] = ball_vel[0] * -1
            ball_acc += 0.3
        else:
            new_game(-1)
    elif ball_pos[1] >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = ball_vel[1] * -1
    elif ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = ball_vel[1] * -1

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

    # update paddle's vertical position, keep paddle on the screen
    if paddleleft_direction == "down" and paddleleft_pos + HALF_PAD_HEIGHT <= HEIGHT:
        paddleleft_pos += paddle_acc * paddleleft_vel
    if paddleleft_direction == "up" and paddleleft_pos - HALF_PAD_HEIGHT >= 0:
        paddleleft_pos += paddle_acc * paddleleft_vel

    if paddleright_direction == "down" and paddleright_pos + HALF_PAD_HEIGHT <= HEIGHT:
        paddleright_pos += paddle_acc * paddleright_vel
    if paddleright_direction == "up" and paddleright_pos - HALF_PAD_HEIGHT >= 0:
        paddleright_pos += paddle_acc * paddleright_vel

    # draw paddles
    canvas.draw_polygon([(0, paddleleft_pos - HALF_PAD_HEIGHT),
                         (0 + PAD_WIDTH, paddleleft_pos - HALF_PAD_HEIGHT),
                         (0 + PAD_WIDTH, paddleleft_pos + HALF_PAD_HEIGHT),
                         (0, paddleleft_pos + HALF_PAD_HEIGHT)
                        ],
                        5, 'White', 'White')
    canvas.draw_polygon([(WIDTH - PAD_WIDTH, paddleright_pos - HALF_PAD_HEIGHT),
                         (WIDTH, paddleright_pos - HALF_PAD_HEIGHT),
                         (WIDTH, paddleright_pos + HALF_PAD_HEIGHT),
                         (WIDTH - PAD_WIDTH, paddleright_pos + HALF_PAD_HEIGHT),
                        ], 5, 'White', 'White')

    # draw scores
    canvas.draw_text(str(scoreleft), [WIDTH / 2 - 100, HEIGHT / 5], 40, "White")
    canvas.draw_text(str(scoreright), [WIDTH / 2 + 100, HEIGHT / 5], 40, "White")


def keydown(key):
    global paddleleft_vel, paddleright_vel, paddleright_direction, paddleleft_direction

    if key == simplegui.KEY_MAP["up"]:
        paddleright_vel = -1
        paddleright_direction = "up"
    if key == simplegui.KEY_MAP["down"]:
        paddleright_vel = 1
        paddleright_direction = "down"
    if key == simplegui.KEY_MAP["w"]:
        paddleleft_vel = -1
        paddleleft_direction = "up"
    if key == simplegui.KEY_MAP["s"]:
        paddleleft_vel = 1
        paddleleft_direction = "down"


def keyup(key):
    global paddleleft_vel, paddleright_vel

    if key == simplegui.KEY_MAP["up"]:
        paddleright_vel = 0
    if key == simplegui.KEY_MAP["down"]:
        paddleright_vel = 0
    if key == simplegui.KEY_MAP["w"]:
        paddleleft_vel = 0
    if key == simplegui.KEY_MAP["s"]:
        paddleleft_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.add_button("Reset", reset_handler, 50)

# start frame
new_game(0)
frame.start()