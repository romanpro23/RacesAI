import math

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
    vertical: bool

    def __init__(self, point_start, point_end):
        self.point_end = point_end
        self.point_start = point_start

        self.update_coefficient()

    def update_coefficient(self):
        xs, ys = self.point_start
        xe, ye = self.point_end

        if xe == xs:
            self.vertical = True
        else:
            self.vertical = False
            self.a = (ye - ys) / (xe - xs)
            self.b = ye - self.a * xe

    def rot(self, angle, central_point):
        cos = math.cos(math.radians(angle))
        sin = math.sin(math.radians(angle))

        xs, ys = self.point_start
        xe, ye = self.point_end
        xc, yc = central_point

        txs = xc + (xs - xc) * cos - (ys - yc) * sin
        tys = yc + (xs - xc) * sin + (ys - yc) * cos

        txe = xc + (xe - xc) * cos - (ye - yc) * sin
        tye = yc + (xe - xc) * sin + (ye - yc) * cos

        self.point_end = (txe, tye)
        self.point_start = (txs, tys)

        self.update_coefficient()

    def check_intersection(self, line):
        xs1, ys1 = self.point_start
        xs2, ys2 = line.point_start
        xe1, ye1 = self.point_end
        xe2, ye2 = line.point_end

        if self.vertical or line.vertical:
            if self.vertical and min(xs2, xe2) <= xs1 <= max(xs2, xe2):
                y = line.a * xs1 + line.b
                return (xs1, y) if min(ys1, ye1) <= y <= max(ys1, ye1) else None
            elif line.vertical and min(xs1, xe1) <= xs2 <= max(xs1, xe1):
                y = self.a * xs2 + self.b
                return (xs2, y) if min(ys2, ye2) <= y <= max(ys2, ye2) else None
            return None

        if self.a != line.a:
            x = (line.b - self.b) / (self.a - line.a)
            y = self.a * x + self.b
            if min(xs1, xe1) <= x <= max(xs1, xe1) and min(xs2, xe2) <= x <= max(xs2, xe2):
                return (x, y)

        return None

    def move(self, dx, dy):
        xs, ys = self.point_start
        xe, ye = self.point_end

        self.point_end = (xe + dx, ye + dy)
        self.point_start = (xs + dx, ys + dy)

        self.update_coefficient()
