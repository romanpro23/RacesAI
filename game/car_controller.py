import os

from ai.agent import Agent
from game.car import Car
from game.environment import Environment


class CarController:
    car: Car
    ai: bool
    agent: Agent

    car_parameters: dict
    frequency_ai: int

    counter: int
    total_score: int

    directions = {
        "up": False,
        "down": False,
        "left": False,
        "right": False,
        "stop": False
    }

    def __init__(self, car: Car, ai: bool = False, agent: Agent = None, frequency_ai: int = 0):
        self.ai = True if agent is not None else ai
        self.frequency_ai = frequency_ai

        self.counter = 0
        self.total_score = 0

        self.agent = agent
        self.car = car

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

    def update(self, environment: Environment):
        if self.ai:
            self.ai_action(environment)

        self.__direction_update()
        self.car.update()

    def ai_action(self, environment):
        if not self.counter % self.frequency_ai == 0:
            self.counter += 1
            return

        self.counter += 1
        self.clear_directions()

        state = environment.get_state(self.car) if self.agent.state is None else self.agent.state

        action = self.agent.action(state)

        if action == 0:
            action = "up"
        elif action == 1:
            action = "down"
        elif action == 2:
            action = "left"
        elif action == 3:
            action = "right"
        else:
            action = "stop"

        self.change_direction(action)

        reward, done = environment.get_reward(self.car)
        next_state = environment.get_state(self.car)

        self.total_score += reward

        self.agent.state = next_state
        self.agent.update(state, action, reward, next_state, done)
        self.agent.train(64, update_epsilon=True)

        if done:
            next_state = None
            restart()

    def restart(self):
        print(self.total_score, self.counter)
        # agent.train(1024, update_epsilon=True)
        if not os.path.exists("/models"):
            os.makedirs("/models")
        self.agent.save(f"models/ai_{self.total_score}")

        self.total_score = 0
        self.counter = 0

        self.agent.state = None
        environment = Environment(generator.frames, generator.rewards, generator.finish, reward_move=0.1,
                                  amount_inactivity=400)
        car = Car(25, 10, max_speed=5, drift_control=0.1, color=RED, x=x, y=y, length_sensor=150)