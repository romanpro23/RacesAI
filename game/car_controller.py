import os

from ai.agent import Agent
from game.car import Car
from game.environment import Environment


class CarController:
    car: Car
    agent: Agent

    ai: bool
    frequency_ai: int

    action: int
    counter: int
    total_score: int
    accumulated_reward: int

    car_parameters: dict

    directions = {
        "up": False,
        "down": False,
        "left": False,
        "right": False,
        "stop": False
    }

    def __init__(self, car: Car, agent: Agent = None, frequency_ai: int = 0):
        self.ai = True if agent is not None else False
        self.frequency_ai = frequency_ai

        self.counter = 0
        self.total_score = 0
        self.action = 0
        self.accumulated_reward = 0

        self.agent = agent
        self.car = car

        self.__fill_car_parameters(car)

    def change_direction(self, direction: str, value: bool = False):
        self.directions[direction] = value

    def clear_directions(self):
        for direction in self.directions.keys():
            self.directions[direction] = False

    def __fill_car_parameters(self, car):
        car_parameters = {"height": car.height,
                          "width": car.width,
                          "acceleration": car.acceleration,
                          "max_speed": car.max_speed,
                          "maneuverability": car.maneuverability,
                          "grip": car.grip,
                          "brakes": car.brakes,
                          "handbrakes": car.handbrakes,
                          "back_speed": car.back_speed,
                          "drift_control": car.drift_control,
                          "color": car.color,
                          "speed_gearbox": car.speed_gearbox,
                          "length_sensor": car.length_sensor,
                          "x": car.x, "y": car.y
                          }

        self.car_parameters = car_parameters

    def __restart_car(self):
        car_parameters = self.car_parameters

        self.car = Car(
            car_parameters["height"],
            car_parameters["width"],
            car_parameters["acceleration"],
            car_parameters["max_speed"],
            car_parameters["maneuverability"],
            car_parameters["grip"],
            car_parameters["brakes"],
            car_parameters["handbrakes"],
            car_parameters["back_speed"],
            car_parameters["drift_control"],
            car_parameters["color"],
            car_parameters["speed_gearbox"],
            car_parameters["length_sensor"],
            car_parameters["x"],
            car_parameters["y"]
        )

        self.counter = 0
        self.total_score = 0

    def __direction_update(self):
        if self.directions["stop"] or (self.directions["up"] and self.directions["down"]):
            self.car.handbrake_stop()
        elif self.directions["up"]:
            self.car.move(1)
        elif self.directions["down"]:
            self.car.move(-1)
        else:
            self.car.move(0)

        if self.directions["left"] and self.directions["right"]:
            self.car.rot(0)
        elif self.directions["left"]:
            self.car.rot(-1)
        elif self.directions["right"]:
            self.car.rot(1)

    def make_action(self, state):
        if self.counter % self.frequency_ai == 0:
            self.ai_action(state)
        self.counter += 1

    def update(self, state, reward, done, next_state=None):
        self.__direction_update()
        self.car.update()

        self.accumulated_reward += reward
        self.total_score += reward

        if (self.counter % self.frequency_ai == (self.frequency_ai - 1) or done) and self.ai:
            self.agent.update(state, self.action, self.accumulated_reward, next_state, done)
            self.agent.train(64, update_epsilon=True)

            self.accumulated_reward = 0

        if done:
            self.restart()

    def ai_action(self, state):
        self.clear_directions()

        self.action = self.agent.action(state)
        self.change_direction(self.get_str_action(self.action), True)

    @staticmethod
    def get_str_action(code_action):
        action = "stop"
        if code_action == 0:
            action = "up"
        elif code_action == 1:
            action = "down"
        elif code_action == 2:
            action = "left"
        elif code_action == 3:
            action = "right"
        return action

    def restart(self):
        print(self.total_score, self.counter)
        if self.ai:
            if not os.path.exists("models"):
                os.makedirs("models")
            self.agent.save(f"models/ai_{self.total_score}")

        self.total_score = 0
        self.counter = 0

        self.clear_directions()
        self.__restart_car()

    def draw(self):
        self.car.draw()
