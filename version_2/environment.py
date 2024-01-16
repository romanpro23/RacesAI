from version_2.car import *
from function.function import *


class Environment:
    accumulated_reward: float
    frames: list
    rewards: list
    finish: Line

    lines: list
    lines_batch: pyglet.graphics.Batch

    counter_action: int
    amount_inactivity: int

    def __init__(self, frames_sides, reward_lines, finish, amount_inactivity=200):
        self.frames = frames_sides
        self.rewards = list(reward_lines)
        self.accumulated_reward = 1
        self.finish = finish

        self.counter_action = 0
        self.amount_inactivity = amount_inactivity

        self.lines = []
        self.lines_batch = pyglet.graphics.Batch()
        self.sensor_points = []
        self.__fill_lines()

    def __fill_lines(self):
        for line in self.frames:
            xs, ys = line.point_start
            xe, ye = line.point_end
            self.lines.append(
                pyglet.shapes.Line(xs, ys, xe, ye, width=2, color=(255, 255, 255), batch=self.lines_batch))

        for line in self.rewards:
            xs, ys = line.point_start
            xe, ye = line.point_end
            self.lines.append(pyglet.shapes.Line(xs, ys, xe, ye, width=2, color=(0, 255, 0), batch=self.lines_batch))

        xs, ys = self.finish.point_start
        xe, ye = self.finish.point_end
        self.lines.append(pyglet.shapes.Line(xs, ys, xe, ye, width=4, color=(255, 255, 0), batch=self.lines_batch))

    def draw(self):
        self.lines_batch.draw()

    def check(self, car: Car):
        for line in self.frames:
            for side in car.body_sides:
                point = line.check_intersection(side)
                if point is not None:
                    return True

        for side in car.body_sides:
            if side.check_intersection(self.finish) is not None and self.rewards:
                return True
        return False

    def get_state(self, car: Car):
        stage = []
        sensor_points = []

        for sensor in car.sensors:
            points = []
            stage_points = []
            for line in self.frames:
                point = sensor.check_intersection(line)
                if point is not None:
                    points.append(point)
                    xs, ys = sensor.point_start
                    xc, yc = point
                    stage_points.append(math.sqrt((xc - xs) ** 2 + (yc - ys) ** 2) / car.length_sensor)

            if len(points) != 0:
                min_value = min(stage_points)
                stage.append(min_value)
                sensor_points.append(points[stage_points.index(min_value)])
            else:
                stage.append(1.0)

        if car.speed > 0:
            stage.append(car.speed / car.max_speed)
        else:
            stage.append(car.speed / car.max_back_speed)

        car.sensors_points = sensor_points
        return stage

    def get_reward(self, car: Car):
        done = self.check(car)
        reward = 0 if not done else -5

        if not done:
            for side in car.body_sides:
                for line in self.rewards:
                    if side.check_intersection(line) is not None:
                        reward = self.accumulated_reward
                        self.accumulated_reward += 0.05
                        self.counter_action = 0

                        self.rewards.remove(line)
                        break

        for side in car.body_sides:
            if side.check_intersection(self.finish) is not None and len(self.rewards) == 0:
                self.accumulated_reward = 0
                reward = 5
                done = True

        self.counter_action += 1
        if self.counter_action > self.amount_inactivity and not done:
            reward = -5
            done = True
            self.counter_action = 0

        if reward == 0:
            if car.speed < 0:
                reward = -0.1
            elif car.speed > 0:
                reward = 0.1

        return reward, done
