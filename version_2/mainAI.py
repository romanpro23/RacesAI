import os
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
car = Car(25, 10, max_speed=5, drift_control=0.1, color=RED, x=x, y=y, length_sensor=150)

next_state = None
epoch = 0
total_score = 0

counter = 0

environment = Environment(generator.frames, generator.rewards, generator.finish)

agent = Agent(epsilon_decay=0.995, action_size=5, epsilon_min=0.02)

direction = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "stop": False
}


def clear_direction():
    direction["up"] = False
    direction["down"] = False
    direction["left"] = False
    direction["right"] = False
    direction["stop"] = False


def change_direction(action: int):
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


def ai_action():
    global total_score
    global next_state

    clear_direction()

    if next_state is None:
        state = environment.get_state(car)
    else:
        state = next_state

    action = agent.action(state)
    change_direction(action)

    reward, done = environment.get_reward(car)
    next_state = environment.get_state(car)

    total_score += reward

    agent.update(state, action, reward, next_state, done)
    agent.train(64, update_epsilon=True)

    if done:
        next_state = None
        restart()


def restart():
    global total_score, epoch, counter
    global environment
    global car
    global next_state

    epoch += 1
    print(epoch, agent.brain.epsilon, len(agent.brain.memory), total_score, counter)
    # agent.train(1024, update_epsilon=True)
    if not os.path.exists("models"):
        os.makedirs("models")
    agent.save(f"models/ai_{total_score}")

    total_score = 0
    counter = 0

    next_state = None
    environment = Environment(generator.frames, generator.rewards, generator.finish)
    car = Car(25, 10, max_speed=5, drift_control=0.1, color=RED, x=x, y=y, length_sensor=150)


def direction_update():
    global car
    if direction["stop"] or (direction["up"] and direction["down"]):
        car.handbrake_stop()
    elif direction["up"]:
        car.move(1)
    elif direction["down"]:
        car.move(-1)
    else:
        car.move(0)

    if direction["left"] and direction["right"]:
        car.rot(0)
    elif direction["left"]:
        car.rot(-1)
    elif direction["right"]:
        car.rot(1)


def update(dt):
    global counter

    ai_action()
    direction_update()

    car.update()


@window.event
def on_draw():
    window.clear()

    background.draw()
    environment.draw()

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
    elif symbol == pyglet.window.key.R:
        pyglet.clock.unschedule(update)
        pyglet.clock.schedule_interval(update, 1.0 / 60)
    elif symbol == pyglet.window.key.E:
        pyglet.clock.unschedule(update)
        pyglet.clock.schedule_interval(update, 1.0 / fps)


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
