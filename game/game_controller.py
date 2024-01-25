import pyglet

from ai.agent import Agent
from function.function import RED
from game.background import Background
from game.car import Car
from game.car_controller import CarController
from game.environment import Environment
from game.level_generator import Generator


class GameController:
    environment: Environment
    car_controller: CarController
    generator: Generator
    background: Background
    agent: Agent

    state: list
    fps: int
    reward_move: float

    def __init__(self, car: Car, agent: Agent = None, level: int = 1, fps=60, width=1024, height=768, frequency_ai=2, reward_move=0.05):
        self.fps = fps
        self.reward_move = reward_move
        self.state = None

        self.generator = Generator(f"maps/map_{level}.txt", width, height)
        self.background = Background(f"maps/background_{level}.png")
        self.environment = Environment(self.generator.frames, self.generator.rewards, self.generator.finish, reward_move=self.reward_move)

        x_car, y_car = self.generator.start_point
        car.set_coordinate(x_car, y_car)

        self.car_controller = CarController(car=car, agent=agent, frequency_ai=frequency_ai)

    def draw(self):
        self.background.draw()
        self.environment.draw()

        self.car_controller.draw()

    def update(self):
        if self.state is None:
            self.state = self.environment.get_state(self.car_controller.car)
            self.car_controller.make_action(self.state)
            return

        reward, done = self.environment.get_reward(self.car_controller.car)
        next_state = self.environment.get_state(self.car_controller.car)

        self.car_controller.update(self.state, reward, done, next_state)
        self.car_controller.make_action(next_state)

        if done:
            self.environment = Environment(self.generator.frames, self.generator.rewards, self.generator.finish,  reward_move=self.reward_move)
        self.state = None if done else next_state

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP or symbol == pyglet.window.key.W:
            self.car_controller.change_direction("up", True)
        elif symbol == pyglet.window.key.DOWN or symbol == pyglet.window.key.S:
            self.car_controller.change_direction("down", True)
        elif symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.A:
            self.car_controller.change_direction("left", True)
        elif symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.D:
            self.car_controller.change_direction("right", True)
        elif symbol == pyglet.window.key.SPACE:
            self.car_controller.change_direction("stop", True)

    def on_key_release(self, symbol, modifiers):
        if symbol == pyglet.window.key.UP or symbol == pyglet.window.key.W:
            self.car_controller.change_direction("up", False)
        elif symbol == pyglet.window.key.DOWN or symbol == pyglet.window.key.S:
            self.car_controller.change_direction("down", False)
        elif symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.A:
            self.car_controller.change_direction("left", False)
        elif symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.D:
            self.car_controller.change_direction("right", False)
        elif symbol == pyglet.window.key.SPACE:
            self.car_controller.change_direction("stop", False)

        if symbol == pyglet.window.key.Q:
            self.car_controller.clear_directions()
            self.car_controller.ai = not self.car_controller.ai
