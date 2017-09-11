# Copyright (c) 2013 David Holm <dholmster@gmail.com>
# This file is part of SimpleGUITk - https://github.com/dholm/simpleguitk
# See the file 'COPYING' for copying permission.

from __future__ import division

import io
import tempfile
import pygame

try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen


class Sound(object):
    def __init__(self, url):
        if url.startswith('http'):
            soundfile = urlopen(url).read()
        else:
            soundfile = open(url).read()

        f = tempfile.NamedTemporaryFile(delete=False)
        f.name
        f.write(soundfile)
        f.close()

        fn = f.name
        # self._sound = pygame.mixer.Sound(file=fn)
        #        pygame.mixer.music.load(fn)
        #pygame.mixer.music.load("C:\\Users\\claube\\appData\\local\\temp\\tmpy8bfqf.mp3")

        self._paused = False

    def play(self):
        pass

    # pygame.mixer.music.play()

    def pause(self):
        pass

    #        pygame.mixer.music.pause()

    def rewind(self):
        pass

    #        pygame.mixer.music.rewind()

    def set_volume(self, volume):
        pass

# pygame.mixer.music.set_volume(volume)

_initialized = False


def sound_init():
    global _initialized
    import pygame

    pygame.mixer.init()
    _initialized = True


def load_sound(URL):
    global _next_channel
    if not _initialized:
        sound_init()

    return Sound(URL)

