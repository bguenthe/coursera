# Pong Game
# Implementation of classic arcade game Pong. This version implements a
# tournament mode which simulates a proper game. First person to score 15
# wins the game.

# include necessary modules
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
LEFT = False
RIGHT = True

# global variable for tournament mode
is_game = False

# event_handlers for the tournament mode
def start_tournament():
    global is_game, ball_pos, ball_vel, is_served

    is_game = True;
    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [0.0, 0.0]
    is_served = False
    new_game()

def serve_ball():
    global is_game, direction, score1, score2

    # disable button if not in tournament mode
    if is_game == False:
        return
    # if game is finished, reset tournament
    elif score1 == 15 or score2 == 15:
        start_tournament()
    else:
        # disable button if ball has been spawned
        if is_served:
            return
        else:
            spawn_ball(direction)

# different sizes for the interface
# buttons are enabled only in tournament mode
def small():
    global is_game, BALL_RADIUS, PAD_HEIGHT, HALF_PAD_HEIGHT

    if is_game:
        BALL_RADIUS = 10
        PAD_HEIGHT = 40
        HALF_PAD_HEIGHT = PAD_HEIGHT / 2
    else:
        return

def medium():
    global is_game, BALL_RADIUS, PAD_HEIGHT, HALF_PAD_HEIGHT

    if is_game:
        BALL_RADIUS = 15
        PAD_HEIGHT = 60
        HALF_PAD_HEIGHT = PAD_HEIGHT / 2
    else:
        return

def large():
    global is_game, BALL_RADIUS, PAD_HEIGHT, HALF_PAD_HEIGHT

    if is_game:
        BALL_RADIUS = 20
        PAD_HEIGHT = 80
        HALF_PAD_HEIGHT = PAD_HEIGHT / 2
    else:
        return

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    global x_direction, y_direction
    global is_game, is_served

    ball_pos = [WIDTH/2, HEIGHT/2]
    ball_vel = [0.0, 0.0]
    ball_vel[0] = float(random.randrange(120, 240)) / 60.0
    ball_vel[1] = float(random.randrange(60, 180)) / 60.0
    y_direction = -1
    is_served = True

    # for the tournament mode, both up and down spawns are randomized
    # overrides the default upward spawn
    if is_game:
        y_direction = random.choice((-1, 1))

    if direction == RIGHT:
        x_direction = 1;
    else:
        x_direction = -1

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global x_direction, y_direction, score1, score2
    global BALL_RADIUS, PAD_HEIGHT, HALF_PAD_HEIGHT
    global is_game, direction

    # default size for the tournament mode (medium)
    if is_game:
        BALL_RADIUS = 15
        PAD_HEIGHT = 60
        HALF_PAD_HEIGHT = PAD_HEIGHT / 2
    else:
        BALL_RADIUS = 20
        PAD_HEIGHT = 80
        HALF_PAD_HEIGHT = PAD_HEIGHT / 2

    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    direction = random.choice((LEFT, RIGHT))

    if is_game == False:
        spawn_ball(direction)

def restart():
    global is_game, score1, score2

    is_game = False
    score1 = 0
    score2 = 0
    new_game()

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global y_direction, x_direction, paddle1_vel, paddle2_vel
    global is_game, direction, is_served


    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], \
                     1, "White")
    # update ball
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT \
                and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] += ball_vel[0] * 0.1
            ball_vel[1] += ball_vel[1] * 0.1
            x_direction *= -1
        else:
            score2 += 1
            direction = RIGHT
            if is_game:
                ball_pos[0] = WIDTH / 2
                ball_pos[1] = HEIGHT / 2
                ball_vel[0] = 0.0
                ball_vel[1] = 0.0
                is_served = False
            else:
                spawn_ball(direction)

    elif ball_pos[0] +  BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT \
                and ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] += ball_vel[0] * 0.1
            ball_vel[1] += ball_vel[1] * 0.1
            x_direction *= -1
        else:
            score1 += 1
            direction = LEFT
            if is_game:
                ball_pos[0] = WIDTH / 2
                ball_pos[1] = HEIGHT / 2
                ball_vel[0] = 0.0
                ball_vel[1] = 0.0
                is_served = False
            else:
                spawn_ball(direction)

    elif ball_pos[1] - BALL_RADIUS  <= 0 or ball_pos[1] + BALL_RADIUS  >= HEIGHT:
        y_direction *= -1

    ball_pos[0] += x_direction * ball_vel[0]
    ball_pos[1] += y_direction * ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel

    if paddle1_pos - HALF_PAD_HEIGHT <= 0:
        paddle1_pos = HALF_PAD_HEIGHT
    elif paddle1_pos + HALF_PAD_HEIGHT >= HEIGHT:
        paddle1_pos = HEIGHT - 1 - HALF_PAD_HEIGHT

    if paddle2_pos - HALF_PAD_HEIGHT <= 0:
        paddle2_pos = HALF_PAD_HEIGHT
    elif paddle2_pos + HALF_PAD_HEIGHT >= HEIGHT:
        paddle2_pos = HEIGHT - HALF_PAD_HEIGHT

    # draw paddles
    canvas.draw_polygon([[0, paddle1_pos - HALF_PAD_HEIGHT], \
                         [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT], \
                         [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT], \
                         [0, paddle1_pos + HALF_PAD_HEIGHT]], \
                        1, "Red", "Red")
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT], \
                         [WIDTH, paddle2_pos - HALF_PAD_HEIGHT], \
                         [WIDTH, paddle2_pos + HALF_PAD_HEIGHT], \
                         [WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT]], \
                        1, "Red", "Red")

    # draw scores
    if is_game:
        if ball_vel[0] == 0.0 and ball_vel[1] == 0.0:
            canvas.draw_text(str(score1), [195, 100], 60, "Teal")
            canvas.draw_text(str(score2), [375, 100], 60, "Teal")
            if score1 == 15:
                canvas.draw_text("Player 1 wins!", [50, 220], 35, "Teal")
            elif score2 == 15:
                canvas.draw_text("Player 2 wins!", [345, 220], 35, "Teal")
    else:
        canvas.draw_text(str(score1), [190, 100], 60, "Teal")
        canvas.draw_text(str(score2), [375, 100], 60, "Teal")

def keydown(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel -= 10
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel += 10
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel -= 10
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel += 10

def keyup(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel += 10
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel -= 10
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel += 10
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel -= 10

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("RESTART", restart, 200)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_label("")
frame.add_label("")
frame.add_label("")
frame.add_label("<- TOURNAMENT MODE ->")
frame.add_label("")
frame.add_button("START TOURNAMENT", start_tournament, 200)
frame.add_button("SERVE BALL", serve_ball, 200)
frame.add_label("")
frame.add_label("Select Interface:")
frame.add_button("Small", small, 200)
frame.add_button("Medium", medium, 200)
frame.add_button("Large", large, 200)



# start frame
new_game()
frame.start()

