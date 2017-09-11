import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

message = "Welcome!"

# Handler for mouse click
def click():
    global message
    message = "Good job!"


# Handler to draw on canvas
def draw(canvas):
    canvas.draw_text(message, [50, 112], 36, "Red")

# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", 600, 400)
frame.add_button("Click me", click)
frame.set_draw_handler(draw)

# Start the frame animation
frame.start()