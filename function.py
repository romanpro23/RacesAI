import math

import function

RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)


def sign(numb):
    return 0 if numb == 0 else abs(numb) / numb


def clip(numb, numb_min, numb_max):
    return min(max(numb, numb_min), numb_max)


class Line:
    point_start: tuple
    point_end: tuple

    a: float
    b: float

    def __init__(self, point_start, point_end):
        self.point_end = point_end
        self.point_start = point_start

        self.update_coefficient()

    def update_coefficient(self):
        xs, ys = self.point_start
        xe, ye = self.point_end

        self.a = (ye - ys) / (xe - xs) if xe - xs != 0 else 0
        self.b = ye - self.a * xe

    def rot(self, angle):
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))

        xs, ys = self.point_start
        xe, ye = self.point_end

        txs = xs * cos - ys * sin
        tys = xs * sin + ys * cos

        txe = xe * cos - ye * sin
        tye = xe * sin + ye * cos

        self.point_end = (txe, tye)
        self.point_start = (txs, tys)

        self.update_coefficient()

    def check_intersection(self, line):
        if self.a != line.a:
            x = (line.b - self.b) / (self.a - line.a)
            y = self.a * x + self.b

            xs, ys = self.point_start
            xe, ye = self.point_end

            if min(xs, xe) <= x <= max(xs, xe):
                return True, (x, y)

        return False, (0, 0)
