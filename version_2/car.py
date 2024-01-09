import pyglet
from pyglet import shapes
from function.function import *
import math


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
    body_sides: list
    sensors: list

    x: float
    y: float
    dx: float
    dy: float
    ds: float
    dfx: float
    dfy: float

    body: shapes.Rectangle
    sensors_lines: list
    sensors_points: list

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
        self.__fill_body_sides()

        length_sensor_45 = length_sensor / math.sqrt(2)
        self.sensors = [
            Line((-self.width // 2, -self.height // 4),
                 (-self.width // 2 - length_sensor_45, -self.height // 4 - length_sensor_45)),
            Line((0, -self.height // 4), (0, -self.height // 4 - length_sensor)),
            Line((self.width // 2, -self.height // 4),
                 (self.width // 2 + length_sensor_45, -self.height // 4 - length_sensor_45)),
            Line((self.width // 2, self.height // 4),
                 (self.width // 2 + length_sensor, self.height // 4)),
            Line((-self.width // 2, self.height // 4),
                 (-self.width // 2 - length_sensor, self.height // 4)),
            Line((-self.width // 2, self.height * 3 // 4),
                 (-self.width // 2 - length_sensor_45, self.height * 3 // 4 + length_sensor_45)),
            Line((0, self.height * 3 // 4), (0, self.height * 3 // 4 + length_sensor)),
            Line((self.width // 2, self.height * 3 // 4),
                 (self.width // 2 + length_sensor_45, self.height * 3 // 4 + length_sensor_45))
        ]

        for line in self.sensors:
            line.move(self.x, self.y)

        self.sensors_points = []
        self.sensors_lines = []
        for line in self.sensors:
            xs, ys = line.point_start
            xe, ye = line.point_end
            line = pyglet.shapes.Line(xs, ys, xe, ye, width=2, color=(255, 255, 255))
            line.anchor_position = (0, 0)
            self.sensors_lines.append(line)


    def __fill_body_sides(self):
        self.body_sides = [
            Line((-self.width // 2 + self.x, -self.height // 4 + self.y),
                 (self.width // 2 + self.x, -self.height // 4 + self.y)),
            Line((-self.width // 2 + self.x, -self.height // 4 + self.y),
                 (-self.width // 2 + self.x, self.height * 3 // 4 + self.y)),
            Line((self.width // 2 + self.x, self.height * 3 // 4 + self.y),
                 (self.width // 2 + self.x, -self.height // 4 + self.y)),
            Line((-self.width // 2 + self.x, self.height * 3 // 4 + self.y),
                 (self.width // 2 + self.x, self.height * 3 // 4 + self.y))
        ]

    def draw(self):
        self.body.draw()

        # for line in self.sensors:
        #     xs, ys = line.point_start
        #     xe, ye = line.point_end
        #     line = pyglet.shapes.Line(xs, ys, xe, ye, width=2, color=(255, 255, 255))
        #
        #     line.draw()

        # for point in self.sensors_points:
        #     x, y = point
        #     p = pyglet.shapes.Circle(x, y, 5, 5, color=(255, 0, 0))
        #     p.draw()
        #     line.delete()

    def move(self, ds):
        self.ds = ds
        if sign(ds) != sign(self.speed):
            ds *= self.brakes
            # self.drift_speed += ds * self.acceleration

        self.speed += ds * self.acceleration

        if not -self.max_back_speed < self.speed < self.max_speed:
            self.speed = clip(self.speed, -self.max_back_speed, self.max_speed)

    def rot_body_point(self, angle):
        for line in self.body_sides:
            line.rot(angle, (self.x, self.y))

    def rot_sensor_point(self, angle):
        for sensor in self.sensors:
            sensor.rot(angle, (self.x, self.y))

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

            self.rot_body_point(da)
            self.rot_sensor_point(da)
            # self.rot_sensor_point(cos, sin)

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
        # cos_a = function.cos(function.radians(90 - self.angle))
        sin = math.sin(math.radians(self.angle))
        # sin_a = function.sin(function.radians(90 - self.angle))

        self.dx = -self.speed * sin
        self.dy = self.speed * cos

        # tx = self.width * cos - self.height * sin
        # ty = self.width * sin + self.height * cos

        self.x += self.dx
        self.y += self.dy

        for side in self.body_sides:
            side.move(self.dx, self.dy)

        for line in self.sensors:
            line.move(self.dx, self.dy)

        for line in self.sensors_lines:
            line.x += self.dx
            line.y += self.dy
            line.rotation = -self.angle

        self.body.x = self.x  # + (self.width - tx) * 0.5
        self.body.y = self.y  # + (self.height - ty) * 0.5

        self.body.rotation = -self.angle
