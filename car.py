import pyglet
from pyglet import shapes
from function import *
import math
import numpy as np
import random


class Car:
    speed: float
    drift_speed: float
    drift_max_speed: float
    drift_control: float

    height: int
    width: int

    acceleration: float
    max_speed: int
    max_back_speed: int
    grip: float
    color: tuple
    angle: float
    brakes: float
    handbrakes: float
    back_speed: float
    maneuverability: float
    speed_gearbox: tuple
    count_gears: int
    gear: int

    length_sensor: int
    body_points: list
    sensor_points: list

    x: float
    y: float
    dx: float
    dy: float
    ds: float
    dfx: float
    dfy: float

    body: shapes.Rectangle

    def __init__(self,
                 height,
                 width,
                 acceleration=0.05,
                 max_speed=5,
                 maneuverability=3,
                 grip=0.005,
                 brakes=1.5,
                 handbrakes=0.95,
                 back_speed=0.25,
                 drift_control=0.5,
                 color=(255, 0, 0),
                 speed_gearbox=(0.2, 0.4, 0.6, 0.8, 1),
                 length_sensor=50,
                 x=384,
                 y=300):

        self.height = height
        self.width = width
        self.color = color

        self.acceleration = acceleration
        self.max_speed = max_speed
        self.grip = grip
        self.maneuverability = maneuverability
        self.brakes = brakes
        self.handbrakes = handbrakes
        self.back_speed = back_speed
        self.max_back_speed = int(max_speed * back_speed)

        self.speed_gearbox = speed_gearbox
        self.count_gears = len(speed_gearbox)
        self.gear = 1

        self.drift_control = drift_control
        self.drift_max_speed = max_speed * (1 - drift_control)

        self.x = x
        self.y = y

        self.dx = 0
        self.dy = 0
        self.ds = 0

        self.angle = 0
        self.speed = 0
        self.drift_speed = 0

        self.body = shapes.Rectangle(x=self.x, y=self.y, width=self.width, height=self.height, color=self.color)
        self.body.anchor_position = (self.width // 2, self.height // 4)

        self.length_sensor = length_sensor
        self.body_points = [
            (-self.width // 2, -self.height // 4),
            (self.width // 2, self.height * 3 // 4),
            (self.width // 2, -self.height // 4),
            (-self.width // 2, self.height * 3 // 4)
        ]

        length_sensor_45 = length_sensor / math.sqrt(2)
        self.sensor_points = [
            ((-self.width // 2, -self.height // 4),
             (-self.width // 2 - length_sensor_45, -self.height // 4 - length_sensor_45)),
            ((0, -self.height // 4), (0, -self.height // 4 - length_sensor)),
            ((self.width // 2, -self.height // 4),
             (self.width // 2 + length_sensor_45, -self.height // 4 - length_sensor_45)),
            ((self.width // 2, self.height // 4),
             (self.width // 2 + length_sensor, self.height // 4)),
            ((-self.width // 2, self.height // 4),
             (-self.width // 2 - length_sensor, self.height // 4)),
            ((-self.width // 2, self.height * 3 // 4),
             (-self.width // 2 - length_sensor_45, self.height * 3 // 4 + length_sensor_45)),
            ((0, self.height * 3 // 4), (0, self.height * 3 // 4 + length_sensor)),
            ((self.width // 2, self.height * 3 // 4),
             (self.width // 2 + length_sensor_45, self.height * 3 // 4 + length_sensor_45))
        ]

    def draw(self):
        self.body.draw()

    def move(self, ds):
        self.ds = ds
        if sign(ds) != sign(self.speed):
            ds *= self.brakes
            # self.drift_speed += ds * self.acceleration

        self.speed += ds * self.acceleration

        if not -self.max_back_speed < self.speed < self.max_speed:
            self.speed = clip(self.speed, -self.max_back_speed, self.max_speed)

    def rot_body_point(self, cos, sin):
        body_point = []

        for point in self.body_points:
            x, y = point
            tx = x * cos - y * sin
            ty = x * sin + y * cos
            body_point.append((tx, ty))

        self.body_points = body_point

    def rot_sensor_point(self, cos, sin):
        sensor_point = []

        for point in self.sensor_points:
            sx, sy = point[0]
            ex, ey = point[1]
            tsx = sx * cos - sy * sin
            tsy = sx * sin + sy * cos
            tex = ex * cos - ey * sin
            tey = ex * sin + ey * cos
            sensor_point.append(((tsx, tsy), (tex, tey)))

        self.sensor_points = sensor_point

    def handbrake_stop(self):
        self.ds = 0
        self.speed *= self.handbrakes
        self.drift_speed *= self.handbrakes

        # if self.drift_control != 1:
        #     self.angle += self.maneuverability * sign(self.angle) * abs(self.drift_speed / self.drift_max_speed)

    def rot(self, da):
        # self.angle -= da * self.maneuverability

        if self.speed != 0:
            da = -da * self.maneuverability * sign(self.speed) * min(1.0,
                                                                     self.speed / self.max_speed * self.maneuverability)
            self.angle += da
            if self.ds == 0:
                self.speed -= sign(self.speed) * self.grip

            cos = math.cos(math.radians(da))
            sin = math.sin(math.radians(da))

            self.rot_body_point(cos, sin)
            self.rot_sensor_point(cos, sin)

        # if sign(da) != sign(self.angle):
        #     # self.drift_speed /= self.handbrakes
        #     self.drift_speed += da * self.acceleration# * abs(self.speed / self.max_speed)
        #     print(self.drift_speed)
        #     self.drift_speed = clip(self.drift_speed, -self.drift_max_speed, self.drift_max_speed)
        # else:
        #     self.drift_speed *= self.handbrakes

        if abs(self.angle) >= 360:
            self.angle -= 360 * sign(self.angle)

    def update(self):
        if self.ds == 0:
            self.speed -= self.grip * sign(self.speed)
        if abs(self.speed) < self.grip:
            self.ds = 0
            self.speed = 0

        # if abs(self.drift_speed) > 0:
        #     self.drift_speed -= self.grip * sign(self.drift_speed)
        # elif abs(self.drift_speed) < self.grip:
        #     self.drift_speed = 0
        #
        # if self.drift_max_speed != 0 and abs(self.drift_speed / self.drift_max_speed) > self.drift_control:
        #     self.angle += sign(self.angle) * self.maneuverability * (1 - self.drift_control) * abs(
        #         self.drift_speed / self.drift_max_speed)
        # print(f"angle {self.angle}")
        cos = math.cos(math.radians(self.angle))
        # cos_a = math.cos(math.radians(90 - self.angle))
        sin = math.sin(math.radians(self.angle))
        # sin_a = math.sin(math.radians(90 - self.angle))

        self.dx = -self.speed * sin
        self.dy = self.speed * cos

        # tx = self.width * cos - self.height * sin
        # ty = self.width * sin + self.height * cos

        self.x += self.dx
        self.y += self.dy

        self.body.x = self.x  # + (self.width - tx) * 0.5
        self.body.y = self.y  # + (self.height - ty) * 0.5

        self.body.rotation = -self.angle
