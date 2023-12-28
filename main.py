import pyglet
from pyglet import shapes
import math

from car import Car
from car2 import Car2

window = pyglet.window.Window(width=1024, height=786, caption='Races AI')
car = Car(25, 10, 0.05, 5, 0.005, 2, 1.5, 0.5, (255, 0, 0))
car2 = Car2(25, 10, 0.05, 5, 0.005, 2, 1.5, 0.5, (0, 255, 0))

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
        car.stop()
        car2.stop()
    elif direction["up"]:
        car.move(-1)
        car2.move(-1)
    elif direction["down"]:
        car.move(1)
        car2.move(1)
    else:
        car.move(0)
        car2.move(0)

    if direction["left"] and direction["right"]:
        car.rot(0)
        car2.rot(0)
    elif direction["left"]:
        car.rot(1)
        car2.rot(1)
    elif direction["right"]:
        car.rot(-1)
        car2.rot(-1)
    else:
        car.rot(0)
        car2.rot(0)

    # car.rot(turn_dir)
    # car.move(speed_dir)

    car.update()
    car2.update()


@window.event
def on_draw():
    window.clear()
    car.draw()
    car2.draw()


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
