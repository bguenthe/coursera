import math
import random

import simpleguitk as simplegui


# globals for user interface
WIDTH = 800
HEIGHT = 600
time = 0.5


def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]


def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


class ImageInfo:
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated


class Utility:
    # debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
    # debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
    debris_info = ImageInfo([320, 240], [640, 480])
    debris_image = simplegui.load_image(
        "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

    # nebula images - nebula_brown.png, nebula_blue.png, ORIGINAL => nebula_blue.f2014.png
    nebula_info = ImageInfo([400, 300], [800, 600])
    nebula_image = simplegui.load_image(
        "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_brown.png")

    # splash image
    splash_info = ImageInfo([200, 150], [400, 300])
    splash_image = simplegui.load_image(
        "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

    # missile image - shot1.png, shot2.png, shot3.png
    missile_info = ImageInfo([5, 5], [10, 10], 3, 60)
    missile_image = simplegui.load_image(
        "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

    # asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
    asteroid_info = ImageInfo([45, 45], [90, 90], 40)
    asteroid_image = simplegui.load_image(
        "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

    # animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
    explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
    explosion_image = simplegui.load_image(
        "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

    # art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    info_ship = ImageInfo([45, 45], [90, 90], 35)
    info_ship_thrusted = ImageInfo([135, 45], [90, 90], 35)
    ship_image = simplegui.load_image(
        "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

    # sound assets purchased from sounddogs.com, please do not redistribute
    soundtrack = simplegui.load_sound(
        "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
    explosion_sound = simplegui.load_sound(
        "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")
    missile_sound = simplegui.load_sound(
        "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
    ship_thrust_sound = simplegui.load_sound(
        "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")


class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.bexplode = False

        self.explode_time = 24
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        if self.bexplode:
            canvas.draw_image(Utility.explosion_image,
                              [Utility.explosion_info.get_center()[0] + Utility.explosion_info.get_size()[0] * (
                              24 - self.explode_time),
                               Utility.explosion_info.get_center()[1]],
                              Utility.explosion_info.get_size(), self.pos, Utility.explosion_info.get_size())
            self.explode_time -= 1
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel

        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        if self.pos[0] >= WIDTH - 1:
            self.pos[0] = 0
        elif self.pos[0] <= 0:
            self.pos[0] = WIDTH - 1

        if self.pos[1] >= HEIGHT - 1:
            self.pos[1] = 0
        elif self.pos[1] <= 0:
            self.pos[1] = HEIGHT - 1

        if self.lifespan > 0:
            self.lifespan -= 1

    def is_collison(self, pos, imageInfo):
        if self.bexplode != True:  # nur wenn ich nicht gerade explodiere
            distance = dist(self.pos, pos)
            if self.radius + imageInfo.get_radius() > distance:
                return True
            else:
                return False

    def explode(self):
        self.bexplode = True
        Utility.explosion_sound.play()

# Ship class
class Ship:
    def __init__(self, pos, vel, angle):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.play_sound = False
        self.angle = angle
        self.angle_vel = 0
        self.image_center_ship = Utility.info_ship.get_center()
        self.image_center_ship_thrusted = Utility.info_ship_thrusted.get_center()
        self.image_size = Utility.info_ship.get_size()
        self.radius = Utility.info_ship.get_radius()

        self.explode_time = 24
        self.bexplode = False

    def draw(self, canvas):
        if self.bexplode:
            canvas.draw_image(Utility.explosion_image,
                              [Utility.explosion_info.get_center()[0] + Utility.explosion_info.get_size()[0] * (
                              24 - self.explode_time),
                               Utility.explosion_info.get_center()[1]],
                              Utility.explosion_info.get_size(), self.pos, Utility.explosion_info.get_size())
            self.explode_time -= 1
        elif self.thrust == False:
            canvas.draw_image(Utility.ship_image, Utility.info_ship.get_center(), Utility.info_ship.get_size(),
                              self.pos, Utility.info_ship.get_size(),
                              self.angle)
        else:
            canvas.draw_image(Utility.ship_image, Utility.info_ship_thrusted.get_center(), Utility.info_ship.get_size(),
                              self.pos, Utility.info_ship.get_size(),
                              self.angle)

    def update(self):
        self.angle += self.angle_vel

        # update accelaration
        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += forward[0] * 0.5
            self.vel[1] += forward[1] * 0.5

        # update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # update friction
        self.vel[0] *= (1 - 0.05)
        self.vel[1] *= (1 - 0.05)

        # check for leaving the area
        if self.pos[0] >= WIDTH - 1:
            self.pos[0] = 0
        elif self.pos[0] <= 0:
            self.pos[0] = WIDTH - 1

        if self.pos[1] >= HEIGHT - 1:
            self.pos[1] = 0
        elif self.pos[1] <= 0:
            self.pos[1] = HEIGHT - 1

        if self.play_sound:
            Utility.ship_thrust_sound.rewind()
            Utility.ship_thrust_sound.play()
        else:
            Utility.ship_thrust_sound.pause()

    def explode(self):
        self.bexplode = True


class RiceRocks:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.started = False
        self.spawn_rock = False

        self.ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0)

        Utility.soundtrack.set_volume(0.2)
        Utility.soundtrack.play()

        self.missiles = set()
        self.rocks = set()

    def keydown(self, key):
        if key == simplegui.KEY_MAP["left"]:
            self.ship.angle_vel = -0.1

        if key == simplegui.KEY_MAP["right"]:
            self.ship.angle_vel = +0.1

        if key == simplegui.KEY_MAP["up"]:
            self.ship.thrust = True
            self.ship.play_sound = True

        if key == simplegui.KEY_MAP["space"]:
            forward = angle_to_vector(self.ship.angle)
            self.missiles.add(Sprite([self.ship.pos[0] + (self.ship.radius * forward[0]),
                                      self.ship.pos[1] + (self.ship.radius * forward[1])],
                                     [self.ship.vel[0] + forward[0] * 6, self.ship.vel[1] + forward[1] * 6], 0, 0,
                                     Utility.missile_image, Utility.missile_info,
                                     Utility.missile_sound))

    def keyup(self, key):
        if key == simplegui.KEY_MAP["left"]:
            self.ship.angle_vel += 0.1

        if key == simplegui.KEY_MAP["right"]:
            self.ship.angle_vel += - 0.1

        if key == simplegui.KEY_MAP["up"]:
            self.ship.thrust = False
            self.ship.play_sound = False

    def draw(self, canvas):
        global time

        # animiate background
        time += 1
        wtime = (time / 4) % WIDTH
        center = Utility.debris_info.get_center()
        size = Utility.debris_info.get_size()
        canvas.draw_image(Utility.nebula_image, Utility.nebula_info.get_center(), Utility.nebula_info.get_size(),
                          [WIDTH / 2, HEIGHT / 2],
                          [WIDTH, HEIGHT])
        canvas.draw_image(Utility.debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
        canvas.draw_image(Utility.debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

        canvas.draw_text("Score: " + str(self.score), [WIDTH - WIDTH / 5, 0 + HEIGHT / 5], 20, "White")
        canvas.draw_text("Lives: " + str(self.lives), [0 + WIDTH / 10, 0 + HEIGHT / 5], 20, "White")

        # draw splash screen if not started
        if not self.started:
            canvas.draw_image(Utility.splash_image, Utility.splash_info.get_center(),
                              Utility.splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                              Utility.splash_info.get_size())
        else:
            if self.spawn_rock == True:
                if len(self.rocks) <= 2:
                    rock = Sprite([random.randrange(0, WIDTH + 1), random.randrange(0, HEIGHT + 1)],
                                  [random.randrange(-1, 2, 2), random.randrange(-1, 2, 2)],
                                  0, 0.1 + random.random() * 0.1 * random.randrange(-1, 2, 2),
                                  Utility.asteroid_image, Utility.asteroid_info)

                    if rock.is_collison(self.ship.pos, Utility.info_ship) == False:
                        self.rocks.add(rock)
                self.spawn_rock = False

            self.ship.draw(canvas)
            self.ship.update()

            if self.ship.bexplode != True:
                for rock in self.rocks:
                    rock.update()
                    rock.draw(canvas)
                    if rock.is_collison(self.ship.pos, Utility.info_ship):
                        rock.explode()
                        self.ship.explode()
                        self.lives -= 1
                        if self.lives == 0:
                            self.__init__()

                delmiss = set()
                delrocks = set()
                for missile in self.missiles:
                    for rock in self.rocks:
                        if missile.lifespan <= 0:
                            delmiss.add(missile)
                        elif missile.is_collison(rock.pos, Utility.asteroid_info):
                            rock.explode()
                            delmiss.add(missile)
                            self.score += 1

                    missile.draw(canvas)
                    missile.update()
                self.missiles.difference_update(delmiss)
                for rock in self.rocks:
                    if rock.explode_time <= 0:
                        delrocks.add(rock)
                self.rocks.difference_update(delrocks)
            else:
                if self.ship.explode_time == 0:
                    self.ship.bexplode == False
                    self.ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0)
                    self.missiles = set()
                    self.rocks = set()

    def click(self, event):
        self.started = True

    def rock_spawner(self):
        self.spawn_rock = True

    def run(self):
        self.frame = simplegui.create_frame("RiceRocks", WIDTH, HEIGHT)

        self.frame.set_draw_handler(self.draw)

        self.frame.set_keydown_handler(self.keydown)
        self.frame.set_keyup_handler(self.keyup)
        self.frame.set_mouseclick_handler(self.click)

        self.timer = simplegui.create_timer(1000.0, self.rock_spawner)
        self.timer.start()
        self.frame.start()


if __name__ == '__main__':
    ricerocks = RiceRocks()
    ricerocks.run()