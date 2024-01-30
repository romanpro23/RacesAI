from game.car import *
from function.function import *


class Environment:
    frame_lines: list
    reward_lines: list
    finish_line: Line

    lines_draw: list
    lines_batch: pyglet.graphics.Batch
    background: pyglet.image

    car_reward_lines: dict

    counter_action: int
    amount_inactivity: int
    forward_reward: float

    def __init__(self, background,  frames_sides, reward_lines, finish, amount_inactivity=400, reward_move=0.01):
        self.frame_lines = frames_sides
        self.reward_lines = list(reward_lines)
        self.image = pyglet.image.load(background)

        self.finish_line = finish

        self.counter_action = 0
        self.forward_reward = reward_move
        self.amount_inactivity = amount_inactivity

        self.car_reward_lines = {}

        self.__fill_lines()

    def __fill_lines(self):
        self.lines_draw = []
        self.lines_batch = pyglet.graphics.Batch()

        for line in self.frame_lines:
            xs, ys = line.point_start
            xe, ye = line.point_end
            self.lines_draw.append(
                pyglet.shapes.Line(xs, ys, xe, ye, width=2, color=(255, 255, 255), batch=self.lines_batch))

        for line in self.reward_lines:
            xs, ys = line.point_start
            xe, ye = line.point_end
            self.lines_draw.append(pyglet.shapes.Line(xs, ys, xe, ye, width=2, color=(0, 255, 0), batch=self.lines_batch))

        xs, ys = self.finish_line.point_start
        xe, ye = self.finish_line.point_end
        self.lines_draw.append(pyglet.shapes.Line(xs, ys, xe, ye, width=4, color=(255, 255, 0), batch=self.lines_batch))

    def draw(self):
        self.image.blit(0, 0)
        # self.lines_batch.draw()

    def check(self, car: Car):
        self.__check_car(car)

        for line in self.frame_lines:
            for side in car.body_sides:
                point = line.check_intersection(side)
                if point is not None:
                    return True

        for side in car.body_sides:
            if side.check_intersection(self.finish_line) is not None and self.car_reward_lines[car]:
                return True

        return False

    def __check_car(self, car: Car):
        if self.car_reward_lines.items().__contains__(car):
            return
        self.car_reward_lines[car] = list(self.reward_lines)

    def get_state(self, car: Car):
        self.check(car)
        stage = []
        sensor_points = []

        for sensor in car.sensors:
            points = []
            distance_stage_points = []
            for line in self.frame_lines:
                point = sensor.check_intersection(line)
                if point is not None:
                    points.append(point)
                    xs, ys = sensor.point_start
                    xc, yc = point
                    distance_stage_points.append(math.sqrt((xc - xs) ** 2 + (yc - ys) ** 2) / car.length_sensor)

            if len(points) != 0:
                min_value = min(distance_stage_points)
                stage.append(min_value)
                sensor_points.append(points[distance_stage_points.index(min_value)])
            else:
                stage.append(1.0)

        if car.speed > 0:
            stage.append(car.speed / car.max_speed)
        else:
            stage.append(car.speed / car.max_back_speed)

        car.sensors_points = sensor_points
        return stage

    def __check_reward_lines(self, car: Car):
        for side in car.body_sides:
            for line in self.car_reward_lines[car]:
                if side.check_intersection(line) is not None:
                    self.counter_action = 0
                    self.car_reward_lines[car].remove(line)
                    return 1
        return 0

    def get_reward(self, car: Car):
        done = self.check(car)
        reward = self.__check_reward_lines(car) if not done else 5 if self.car_reward_lines[car] else -5

        self.counter_action += 1
        if self.counter_action > self.amount_inactivity and not done:
            reward = -5
            done = True
            self.counter_action = 0

        if reward == 0:
            if car.speed > 0:
                reward = self.forward_reward
            elif car.speed <= 0:
                reward = -self.forward_reward

        return reward, done
