import pygame
import urllib2
import io

pygame.mixer.init()

try:
    pygame.mixer.music.load('c:\\temp\\maniacs.mp3')
    pygame.mixer.music.play(0)

    print pygame.mixer.music.get_busy()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    soundfile = urllib2.urlopen("http://commondatastorage.googleapis.com/codeskulptor-assets/Tetris-Theme-Original.mp3").read()
    bytes = io.BytesIO(soundfile).getvalue()
    try:
        # sound = pygame.mixer.Sound("c:\\temp\\maniacs.mp3")
        sound = pygame.mixer.Sound("c:/temp/f.mp3")
    except pygame.error, message:
        print "SoundError"

    sound.play(loops=-1)
except:
    print "error"

# >>> import pygame
    # >>> pygame.mixer.init()
    # >>> pygame.mixer.music.load("c:\\temp\\maniacs.mp3")
    # >>> pygame.mixer.music.play(0)
    # >>> pygame.mixer.music.play(-1)
    # >>> pygame.mixer.music.load("c:\\temp\\maniacs.mp3")
    # >>> pygame.mixer.music.play(-1)
    # >>> pygame.mixer.music.stop()
    # >>> pygame.mixer.music.play(-1)
    # >>> pygame.mixer.music.stop()
#
# Debugger connected.
#          >>> pygame.mixer.music.play(-1)
#              >>> pygame.mixer.music.stop()
#                  >>> pygame.mixer.music.play(0)
#                      >>> pygame.mixer.music.get_busy()
# 1
# >>> pygame.mixer.music.stop()