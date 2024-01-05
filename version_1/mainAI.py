import pyglet
from PIL import Image
import numpy as np

from background import Background
from version_1.environment import Environment
from function import *

from version_1.car import Car
from agent import Agent

screen = pyglet.canvas.get_display().get_default_screen()
screen_width, screen_height = screen.width, screen.height

window_width, window_height = 1024, 768

x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

window = pyglet.window.Window(width=window_width, height=window_height, caption='Races AI')
window.set_location(x, y)

background = Background("background_1.png")
environment = Environment(background.map)

fps = 1000
fps_agent = 20
counter_fps_agent = 0

pre_state: np.array = None
action: np.array
pre_reward: np.array
pre_action: np.array
epoch = 0

car = Car(25, 10, max_speed=5, drift_control=0.1, color=RED, x=150)

agent = Agent(epsilon_decay=0.99, action_size=4)

direction = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "stop": False
}


def agent_action():
    global action
    global pre_reward
    global pre_action
    global pre_state
    global car
    global direction

    direction["up"] = False
    direction["down"] = False
    direction["left"] = False
    direction["right"] = False
    direction["stop"] = False

    state, reward = environment.get_state(car)
    action = agent.action(state)

    if action == 0:
        direction["up"] = True
    # elif action == 1:
    #     direction["down"] = True
    elif action == 1:
        direction["left"] = True
    elif action == 2:
        direction["right"] = True
    # elif action == 3:
    #     direction["stop"] = True

    if pre_state is not None:
        # print(pre_reward)
        agent.update(pre_state, pre_action, pre_reward, state, 0)
        # agent.train(64, update_epsilon=True)

    pre_state = state
    pre_reward = np.array(reward)
    pre_action = np.array(action)


def update(dt):
    global car
    global counter_fps_agent
    global fps_agent
    global epoch
    global environment

    if counter_fps_agent == 0:
        agent_action()
    else:
        counter_fps_agent += 1
        if counter_fps_agent > fps_agent:
            counter_fps_agent = 0

    if not background.check(car):
        car.update()
    else:
        agent.update(pre_state, pre_action, np.array(-100), pre_state, 1)
        print(pre_state, pre_action, np.array(-100), pre_state, 1)
        agent.train(1024, update_epsilon=True)

        epoch += 1
        print(epoch, agent.brain.epsilon, len(agent.brain.memory))

        environment = Environment(background.map)
        car = Car(25, 10, max_speed=5, drift_control=0.1, color=RED, x=150)

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


@window.event
def on_draw():
    window.clear()
    background.draw()

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
