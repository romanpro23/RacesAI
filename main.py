import pyglet
from pyglet import shapes
import math

from car import Car
from car2 import Car2

window = pyglet.window.Window(width=1024, height=786, caption='Races AI')
cars = [Car(25, 10, 0.05, 5, 0.005, 3, 1.5, 0.5, (255, 0, 0)), Car(25, 10, 0.05, 5, 0.005, 3, 1.5, 1, (0, 255, 0))]

direction = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "stop": False
}


def update(dt):
    global speed_dir
    global turn_dir

    if direction["stop"] or (direction["up"] and direction["down"]):
        for car in cars: car.stop()
    elif direction["up"]:
        for car in cars: car.move(-1)
    elif direction["down"]:
        for car in cars: car.move(1)
    else:
        for car in cars: car.move(0)

    if direction["left"] and direction["right"]:
        for car in cars: car.rot(0)
    elif direction["left"]:
        for car in cars: car.rot(1)
    elif direction["right"]:
        for car in cars: car.rot(-1)
    else:
        for car in cars: car.rot(0)

        # car.rot(turn_dir)
        # car.move(speed_dir)

    for car in cars: car.update()


@window.event
def on_draw():
    window.clear()
    for car in cars: car.draw()


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


pyglet.clock.schedule_interval(update, 1 / 60)
pyglet.app.run()
