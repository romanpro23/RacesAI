import math

import numpy as np


class Environment:
    map: np.array
    reward: int

    def __init__(self, map: np.array):
        self.map = np.array(map)
        print("Init")
        print(self.map.min())
        print(self.map.max())

    def get_reward(self, car):
        reward = 0.0
        state = []

        for sensor in car.sensor_points:
            sx, sy = sensor[0]
            ex, ey = sensor[1]

            state_point = 1

            if ex != sx:
                # l = ex - sx
                # m = ey - sy
                a = - (ey - sy) / (ex - sx)
                b = (sx * ey - sy * ex) / (ex - sx)
                dx = (ex - sx) / car.length_sensor

                for x in np.arange(sx, ex, dx):
                    y = a * x + b

                    tx = int(x + car.x)
                    ty = int(y + car.y)

                    if self.map[-ty][tx] == 1:
                        reward += 1.0 / car.length_sensor
                        self.map[-ty][tx] = 0.5
                    elif self.map[-ty][tx] == 0:
                        state_point = math.sqrt((y - sy) ** 2 + (x - sx) ** 2) / \
                                       math.sqrt((ey - sy) ** 2 + (ex - sx) ** 2)
                        break
            else:
                dy = (ey - sy) / car.length_sensor

                for y in np.arange(sy, ey, dy):
                    tx = int(ex + car.x)
                    ty = int(y + car.y)

                    if self.map[-ty][tx] == 1:
                        reward += 1.0 / car.length_sensor
                        self.map[-ty][tx] = 0.5
                    elif self.map[-ty][tx] == 0:
                        state_point = abs(y - sy) / abs(ey - sy)
                        break

            state.append(state_point)

        print(self.map.shape)
        print(self.map.max())
        return state, reward
