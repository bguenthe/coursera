# template for "Stopwatch: The Game"

import simpleguitk as simplegui

# define global variables
timer_value = 0  # in 10th of a second
stop_attempts = 0
stop_success = 0
start = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    minutes = t / 60 / 1000
    sec = (t / 1000) % 60
    strsec = str(sec)
    if len(strsec) == 1:
        strsec = '0' + strsec
    tens = (t % 1000) / 100
    return str(str(minutes) + ":" + strsec + "." + str(tens))


def start_handler():
    global start, timer_value

    start = True


def stop_handler():
    global start, stop_success, stop_attempts

    if start:
        start = False
        stop_attempts += 1
        if (timer_value % 1000) == 0:
            stop_success += 1


def reset_handler():
    global start, timer_value, stop_attempts, stop_success

    start = False
    timer_value = 0
    stop_attempts = 0
    stop_success = 0


def timer_handler():
    global timer_value
    if start:
        timer_value += 100  # 100 Milli


def draw_handler(canvas):
    canvas.draw_text(format(timer_value), [95, 115], 32, "White")
    canvas.draw_text(str(stop_success) + "/" + str(stop_attempts), [260, 30], 15, "Red")


frame = simplegui.create_frame("Stopwatch", 300, 200)
frame.set_draw_handler(draw_handler)

frame.add_button("Start", start_handler, 50)
frame.add_button("Stop", stop_handler, 50)
frame.add_button("Reset", reset_handler, 50)

timer = simplegui.create_timer(100, timer_handler)
timer.start()

frame.start()