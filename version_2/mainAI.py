import random

import pyglet
from PIL import Image
import numpy as np

from ai.agent import Agent
from version_2.background import Background
from version_2.environment import Environment
from function.function import *

from version_2.car import Car
from version_2.level_generator import Generator

screen = pyglet.canvas.get_display().get_default_screen()
screen_width, screen_height = screen.width, screen.height

window_width, window_height = 1024, 768

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

window = pyglet.window.Window(width=window_width, height=window_height, caption='Races AI')
window.set_location(x, y)

generator = Generator("maps/map_1.txt", window_width, window_height)
background = Background("maps/background_1.png")

fps = 120
x, y = generator.start_point
cars = [
    Car(25, 10, max_speed=5, drift_control=0.1, color=RED, x=x, y=y, length_sensor=200)
]

environment = Environment(generator.frames, generator.rewards, generator.finish)

agent = Agent(epsilon_decay=0.999, action_size=5)

direction = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "stop": False
}

counter = 0
reward: np.array = None

epoch = 0
total_score = 0


def clear_direction():
    direction["up"] = False
    direction["down"] = False
    direction["left"] = False
    direction["right"] = False
    direction["stop"] = False


def change_direction(action):
    if action == 0:
        direction["up"] = True
    elif action == 1:
        direction["down"] = True
    elif action == 2:
        direction["left"] = True
    elif action == 3:
        direction["right"] = True
    else:
        direction["stop"] = True


def agent_action(car):
    global reward
    global counter
    global total_score

    clear_direction()

    state = environment.get_state(car)
    action = agent.action(state)

    change_direction(action)
    reward = environment.get_reward(car)

    if reward is not None:
        total_score += reward

        if reward == 0:
            reward = -0.1 * (counter / fps)
            counter += 1
            if reward <= -1:
                return restart(-1, car)
        elif reward == 20:
            return restart(20, car)
        else:
            counter = 0

        agent.update(reward, state, 0)
        agent.train(32, update_epsilon=True)


def restart(last_reward, car):
    global counter, environment, epoch, total_score
    global reward

    reward = None
    epoch += 1
    print(epoch, agent.brain.epsilon, len(agent.brain.memory), total_score)
    total_score = 0
    counter = 0

    agent.update(np.array(last_reward), None, 1)
    # agent.train(1024, update_epsilon=True)

    environment = Environment(generator.frames, generator.rewards, generator.finish)
    cars.remove(car)
    cars.append(Car(25, 10, max_speed=5, drift_control=0.1, color=RED, x=x, y=y, length_sensor=200))


def direction_update():
    if direction["stop"] or (direction["up"] and direction["down"]):
        for car in cars: car.handbrake_stop()
    elif direction["up"]:
        for car in cars: car.move(1)
    elif direction["down"]:
        for car in cars: car.move(-1)
    else:
        for car in cars: car.move(0)

    if direction["left"] and direction["right"]:
        for car in cars: car.rot(0)
    elif direction["left"]:
        for car in cars: car.rot(-1)
    elif direction["right"]:
        for car in cars: car.rot(1)


def update(dt):
    global counter, environment
    global epoch

    for car in cars:
        agent_action(car)

        if not environment.check(car):
            car.update()
        else:
            restart(-10, car)

    direction_update()


@window.event
def on_draw():
    window.clear()
    background.draw()
    environment.draw()

    for car in cars:
        car.draw()


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.UP or symbol == pyglet.window.key.W:
        direction["up"] = True
    elif symbol == pyglet.window.key.DOWN or symbol == pyglet.window.key.S:
        direction["down"] = True
    elif symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.A:
        direction["left"] = True
    elif symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.D:
        direction["right"] = True
    elif symbol == pyglet.window.key.SPACE:
        direction["stop"] = True
    elif symbol == pyglet.window.key.Q:
        image_pil = Image.fromarray(np.ceil(environment.map * 255).astype(np.uint8))
        image_pil.save('output_image.png')


@window.event
def on_key_release(symbol, modifiers):
    if symbol == pyglet.window.key.UP or symbol == pyglet.window.key.W:
        direction["up"] = False
    elif symbol == pyglet.window.key.DOWN or symbol == pyglet.window.key.S:
        direction["down"] = False
    elif symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.A:
        direction["left"] = False
    elif symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.D:
        direction["right"] = False
    elif symbol == pyglet.window.key.SPACE:
        direction["stop"] = False


pyglet.clock.schedule_interval(update, 1.0 / fps)
pyglet.app.run()
