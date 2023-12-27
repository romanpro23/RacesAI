import pyglet
from pyglet import shapes
import math

from car import Car

window = pyglet.window.Window(width=400, height=400, caption='Races AI')
key_pressed = False
car = Car(50, 20, 0.05, 1, 2, (255, 0, 0))

speed_pressed = False
speed_dir = 0
turn_pressed = False
turn_dir = 0


def update(dt):
    global speed_dir
    global turn_dir

    if turn_dir == 1:
        car.rot(1)
    elif turn_dir == -1:
        car.rot(-1)

    if speed_dir == 1:
        car.move(-1)
    elif speed_dir == -1:
        car.move(1)

    car.update()

@window.event
def on_draw():
    window.clear()
    car.draw()


@window.event
def on_key_press(symbol, modifiers):
    global speed_dir
    global turn_dir
    global speed_pressed
    global turn_pressed

    if not speed_pressed:
        if symbol == pyglet.window.key.UP or symbol == pyglet.window.key.W:
            speed_dir = 1
        elif symbol == pyglet.window.key.DOWN or symbol == pyglet.window.key.S:
            speed_dir = -1

    if not turn_pressed:
        if symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.A:
            turn_dir = 1
        elif symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.D:
            turn_dir = -1


@window.event
def on_key_release(symbol, modifiers):
    global speed_dir
    global turn_dir
    global speed_pressed
    global turn_pressed

    print((symbol == pyglet.window.key.UP or symbol == pyglet.window.key.W or
            symbol == pyglet.window.key.DOWN or symbol == pyglet.window.key.S))
    if (symbol == pyglet.window.key.UP or symbol == pyglet.window.key.W or
            symbol == pyglet.window.key.DOWN or symbol == pyglet.window.key.S):
        speed_dir = 0
        speed_dir = False

    if (symbol == pyglet.window.key.LEFT or symbol == pyglet.window.key.A or
            symbol == pyglet.window.key.RIGHT or symbol == pyglet.window.key.D):
        turn_dir = 0
        turn_pressed = False


# Додати функцію для оновлення гри кожен кадр
pyglet.clock.schedule_interval(update, 1 / 60)

pyglet.app.run()
