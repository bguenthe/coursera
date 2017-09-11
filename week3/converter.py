import simpleguitk as simplegui

draw_text = ""


def draw_handler(canvas):
    global draw_text
    canvas.draw_text(draw_text, [100, 100], 24, "Red")


def input_handler(input):
    global draw_text
    draw_text = input


frame = simplegui.create_frame("Converter", 300, 200)

frame.set_draw_handler(draw_handler)
frame.add_input("DrawText", input_handler, 50)

frame.start()