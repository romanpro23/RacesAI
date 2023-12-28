import pyglet
from pyglet import shapes
import math


class Car2:
    speed: float
    drift_speed: float
    drift_max_speed: float
    height: int
    width: int
    acceleration: float
    max_speed: int
    grip: float
    color: tuple
    angle: float
    brakes: float
    maneuverability: float

    x: float
    y: float
    dx: float
    dy: float
    da: float
    ds: float
    dfx: float
    dfy: float

    body: shapes.Rectangle

    def __init__(self, height, width, acceleration, max_speed, grip, maneuverability, brakes, drift_control, color):
        self.grip = grip
        self.height = height
        self.width = width
        self.acceleration = acceleration
        self.max_speed = max_speed
        self.color = color
        self.maneuverability = maneuverability
        self.brakes = brakes
        self.drift_max_speed = max_speed * (1 - drift_control)

        self.x = 300
        self.y = 384
        self.dx = 0
        self.dy = 0
        self.da = 0
        self.ds = 0
        self.angle = 0
        self.speed = 0
        self.drift_speed = 0

        self.body = shapes.Rectangle(x=self.x, y=self.y, width=self.width, height=self.height, color=self.color)

    def draw(self):
        self.body.draw()

    def sign(self, numb):
        return 0 if numb == 0 else abs(numb) / numb

    def move(self, ds):
        self.ds = ds
        if self.sign(self.ds) != self.sign(self.speed):
            self.ds *= self.brakes

        self.speed += self.ds * self.acceleration

        if abs(self.speed) > self.max_speed:
            self.speed = self.max_speed * self.sign(self.speed)

    def stop(self):
        self.ds = 0
        self.speed *= (1 - self.acceleration)

    def rot(self, da):
        if abs(self.speed) > 0:
            self.da = da * self.maneuverability
            self.angle -= self.da * self.sign(self.ds)

        if self.sign(self.da) == self.sign(self.angle):
            self.drift_speed += self.da * self.grip * abs(self.speed / self.max_speed)
            if abs(self.drift_speed) >= self.drift_max_speed:
                self.drift_speed = self.drift_max_speed * self.sign(self.drift_speed)
        else:
            self.drift_speed *= (1 - self.acceleration)

        if abs(self.angle) >= 360:
            self.angle -= 360 * self.sign(self.angle)

    def update(self):
        if abs(self.speed) < self.grip:
            self.ds = 0
            self.speed = 0

        if abs(self.drift_speed) < self.grip:
            self.drift_speed = 0

        if self.ds == 0:
            self.speed -= self.grip * self.sign(self.speed)

        # if self.speed >= 0.8 * self.max_speed:
        #     self.angle -= self.da * self.sign(self.ds)

        cos = math.cos(math.radians(self.angle))
        cos90 = math.cos(math.radians(90 - self.angle))
        sin = math.sin(math.radians(self.angle))
        sin90 = math.sin(math.radians(90 - self.angle))

        self.dx = self.speed * sin# + sin90 * self.drift_speed
        self.dy = self.speed * -cos# + cos90 * self.drift_speed
        #print(self.drift_speed)

        tx = self.width * cos - self.height * sin
        ty = self.width * sin + self.height * cos

        self.x += self.dx
        self.y += self.dy

        self.body.x = self.x + (self.width - tx) * 0.5
        self.body.y = self.y + (self.height - ty) * 0.5

        self.body.rotation = -self.angle