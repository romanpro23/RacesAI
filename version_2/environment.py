import math

import numpy as np
import pyglet
from PIL import Image
import json

from version_2.car import *
from function import *


class Environment:
    reward: int
    frames: list
    rewards: list
    finish: Line

    lines: list
    lines_batch: pyglet.graphics.Batch

    def __init__(self, frames_sides, reward_lines, finish):
        self.frames = frames_sides
        self.rewards = reward_lines
        self.finish = finish

        self.lines = []
        self.lines_batch = pyglet.graphics.Batch()
        self.__fill_lines()

    def __fill_lines(self):
        for line in self.frames:
            xs, ys = line.point_start
            xe, ye = line.point_end
            self.lines.append(pyglet.shapes.Line(xs, ys, xe, ye, width=2, color=(255, 255, 255), batch=self.lines_batch))

        for line in self.rewards:
            xs, ys = line.point_start
            xe, ye = line.point_end
            self.lines.append(pyglet.shapes.Line(xs, ys, xe, ye, width=2, color=(0, 255, 0), batch=self.lines_batch))

        xs, ys = self.finish.point_start
        xe, ye = self.finish.point_end
        self.lines.append(pyglet.shapes.Line(xs, ys, xe, ye, width=4, color=(255, 255, 0), batch=self.lines_batch))

    def draw(self):
        self.lines_batch.draw()
        # for line in self.lines:
        #     line.draw()

    def check(self, car: Car):
        for line in self.frames:
            for side in car.body_sides:
                point = line.check_intersection(side)
                if point is not None:
                    return True
        return False

    def get_state(self, car):
        reward = 0.0
        state = []

        for sensor in car.sensors:
            sx, sy = sensor[0]
            ex, ey = sensor[1]

            state_point = 1

            l = ex - sx
            m = ey - sy
            st = 0
            if ey - sy != 0:
                et = (ey - sy) / m
            else:
                et = (ex - sx) / l
            dt = et / car.length_sensor

            for t in np.arange(st, et, dt):
                x = sx + l * t
                y = sy + m * t
                tx = int(x + car.x)
                ty = int(y + car.y)

                if self.map[-ty][tx] == 1:
                    reward += 1.0 / car.length_sensor
                    self.map[-ty][tx] = 0.5
                elif self.map[-ty][tx] == 0:
                    state_point = math.sqrt((y - sy) ** 2 + (x - sx) ** 2) / \
                                  math.sqrt((ey - sy) ** 2 + (ex - sx) ** 2)
                    break

            state.append(state_point)

        state.append(car.speed / car.max_speed)

        return state, reward
