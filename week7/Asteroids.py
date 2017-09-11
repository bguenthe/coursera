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
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
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
        distance = dist(self.pos, pos)
        if self.radius + imageInfo.get_radius() > distance:
            return True
        else:
            return False

    def respawn(self):
        self.pos[0] = random.randrange(0, WIDTH + 1)
        self.pos[1] = random.randrange(0, HEIGHT + 1)
        self.vel[0] = random.randrange(-1, 2, 2)
        self.vel[1] = random.randrange(-1, 2, 2)
        self.angle_vel = random.randrange(-1, 2, 2) / 10.0


# Ship class
class Ship:
    def __init__(self, pos, vel, angle):
        # art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
        self.info_ship = ImageInfo([45, 45], [90, 90], 35)
        self.info_ship_thrusted = ImageInfo([135, 45], [90, 90], 35)
        self.image = simplegui.load_image(
            "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")
        self.ship_thrust_sound = simplegui.load_sound(
            "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")

        self.ship_thrust_sound.set_volume(.5)

        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.play_sound = False
        self.angle = angle
        self.angle_vel = 0
        self.image_center_ship = self.info_ship.get_center()
        self.image_center_ship_thrusted = self.info_ship_thrusted.get_center()
        self.image_size = self.info_ship.get_size()
        self.radius = self.info_ship.get_radius()

    def draw(self, canvas):
        if self.thrust == False:
            canvas.draw_image(self.image, self.image_center_ship, self.image_size, self.pos, self.image_size,
                              self.angle)
        else:
            canvas.draw_image(self.image, self.image_center_ship_thrusted, self.image_size, self.pos, self.image_size,
                              self.angle)

    def update(self):
        self.angle += self.angle_vel

        # update accelaration
        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += forward[0]
            self.vel[1] += forward[1]

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
            self.ship_thrust_sound.play()
        else:
            self.ship_thrust_sound.rewind()


class Asteroids:
    def __init__(self):

        # debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
        # debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
        self.debris_info = ImageInfo([320, 240], [640, 480])
        self.debris_image = simplegui.load_image(
            "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

        # nebula images - nebula_brown.png, nebula_blue.png
        self.nebula_info = ImageInfo([400, 300], [800, 600])
        self.nebula_image = simplegui.load_image(
            "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

        # splash image
        self.splash_info = ImageInfo([200, 150], [400, 300])
        self.splash_image = simplegui.load_image(
            "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

        # missile image - shot1.png, shot2.png, shot3.png
        self.missile_info = ImageInfo([5, 5], [10, 10], 3, 60)
        self.missile_image = simplegui.load_image(
            "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

        # asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
        self.asteroid_info = ImageInfo([45, 45], [90, 90], 40)
        self.asteroid_image = simplegui.load_image(
            "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

        # animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
        self.explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
        self.explosion_image = simplegui.load_image(
            "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

        # sound assets purchased from sounddogs.com, please do not redistribute
        self.soundtrack = simplegui.load_sound(
            "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
        self.missile_sound = simplegui.load_sound(
            "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
        self.missile_sound.set_volume(.5)

        self.explosion_sound = simplegui.load_sound(
            "http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

        self.score = 0
        self.lives = 3

        self.ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0)
        self.rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0.1, self.asteroid_image, self.asteroid_info)

        self.missiles = []

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

            self.missiles.append(Sprite([self.ship.pos[0] + (self.ship.radius * forward[0]),
                                         self.ship.pos[1] + (self.ship.radius * forward[1])],
                                        [self.ship.vel[0] + forward[0] * 2, self.ship.vel[1] + forward[1] * 2], 0, 0,
                                        self.missile_image, self.missile_info,
                                        self.missile_sound))

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
        center = self.debris_info.get_center()
        size = self.debris_info.get_size()
        canvas.draw_image(self.nebula_image, self.nebula_info.get_center(), self.nebula_info.get_size(),
                          [WIDTH / 2, HEIGHT / 2],
                          [WIDTH, HEIGHT])
        canvas.draw_image(self.debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
        canvas.draw_image(self.debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

        canvas.draw_text("Score: " + str(self.score), [WIDTH - WIDTH / 5, 0 + HEIGHT / 5], 20, "White")
        canvas.draw_text("Lives: " + str(self.lives), [0 + WIDTH / 10, 0 + HEIGHT / 5], 20, "White")

        # draw ship and sprites
        self.ship.draw(canvas)

        if self.rock.is_collison(self.ship.pos, self.ship.info_ship):
            pass
        self.rock.draw(canvas)

        # update ship and sprites
        self.ship.update()
        self.rock.update()

        delmissiles = []
        for missile in self.missiles:
            if missile.lifespan <= 0:
                delmissiles.append(missile)

        for delmissile in delmissiles:
            self.missiles.remove(delmissile)

        for missile in self.missiles:
            missile.draw(canvas)
            missile.update()


    def rock_spawner(self):
        self.rock.respawn()

    def run(self):
        self.frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

        self.frame.set_draw_handler(self.draw)

        self.frame.set_keydown_handler(self.keydown)
        self.frame.set_keyup_handler(self.keyup)

        self.timer = simplegui.create_timer(100000.0, self.rock_spawner)
        self.timer.start()
        self.frame.start()


if __name__ == '__main__':
    asteroids = Asteroids()
    asteroids.run()