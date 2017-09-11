import simpleguitk as simplegui
import math
import random

message = "Hi"
position = [0, 0]
height = 300
width = 300


def timer_handler():
    x = random.randrange(0, height)
    y = random.randrange(0, width)
    position[0] = x
    position[1] = y
    print(position)


def draw_handler(canvas):
    canvas.draw_text(message, position, 22, "Red")


def input_handler(input):
    global message
    message = input


frame = simplegui.create_frame("Screensaver", height, width)

frame.set_draw_handler(draw_handler)

timer = simplegui.create_timer(2000, timer_handler)
timer.start()

text = frame.add_input("Text", input_handler, 50)
frame.start()

