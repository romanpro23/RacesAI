import pyglet
from pyglet import shapes
import math


class Car:
    speed: float
    height: int
    width: int
    acceleration: float
    max_speed: int
    grip: float
    color: tuple
    angle: float

    x: float
    y: float
    dx: float
    dy: float
    da: float

    body: shapes.Rectangle

    def __init__(self, height, width, acceleration, max_speed, grip, color):
        self.grip = grip
        self.height = height
        self.width = width
        self.acceleration = acceleration
        self.max_speed = max_speed
        self.color = color

        self.x = 100
        self.y = 100
        self.dx = 0
        self.dy = 0
        self.da = 0
        self.angle = 0
        self.speed = 0

        self.body = shapes.Rectangle(x=self.x, y=self.y, width=self.width, height=self.height, color=self.color)

    def draw(self):
        self.body.draw()

    def move(self, ds):
        self.speed += ds * self.acceleration

    def rot(self, da):
        self.da = da
        self.angle += da

    def update(self):
        cos = math.cos(self.angle)
        sin = math.sin(self.angle)
        self.dx = self.speed * sin
        self.dy = self.speed * cos

        tx = self.width * cos + self.height * sin
        ty = -self.width * sin + self.height * cos

        self.x += self.dx
        self.y += self.dy
        print(tx, ty)
        self.body.x = self.x - tx + self.width
        self.body.y = self.y - ty + self.height

        self.body.rotation = -self.angle