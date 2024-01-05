import math

import numpy as np
from PIL import Image


class Environment:
    map: np.array
    reward: int

    def __init__(self, image):
        img = Image.open(image)
        self.map = np.array(img, dtype=np.float32)
        print(self.map.shape)
        print(self.map[455][160])
        print(self.map[342][160])
        print(self.map[1][1])
        print(self.map.max())

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
