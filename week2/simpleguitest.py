import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Event handler
def tick():
    print("tick!")

# Register handler
timer = simplegui.create_timer(1000, tick)

# Start timer
timer.start()