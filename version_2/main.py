import pyglet
from PIL import Image
import numpy as np

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

fps = 60
x, y = generator.start_point
cars = [
    # Car(25, 10, drift_control=1, color=GREEN),
    # Car(25, 10, drift_control=0.75, color=PURPLE),
    # Car(25, 10, drift_control=0.5, color=RED),
    # Car(25, 10, drift_control=0.25, color=BLUE),
    Car(25, 10, max_speed=5, drift_control=0.1, color=RED, x=x, y=y, length_sensor=100)
]

environment = Environment(generator.frames, generator.rewards, generator.finish)

direction = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "stop": False
}

counter = 0
fps_check = 3


def update(dt):
    global counter
    for car in cars:
        environment.get_state(car)
        if environment.check(car):
            car.body.color = (0, 0, 0)
        else:
            car.body.color = (255, 0, 0)
        car.update()

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


@window.event
def on_draw():
    window.clear()
    background.draw()
    environment.draw()

    for car in cars:
        car.draw()
        # environment.get_reward(car)
        # print(environment.get_state(car))


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
