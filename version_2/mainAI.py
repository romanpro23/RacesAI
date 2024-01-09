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

fps = 600
x, y = generator.start_point
cars = [
    # Car(25, 10, drift_control=1, color=GREEN),
    # Car(25, 10, drift_control=0.75, color=PURPLE),
    # Car(25, 10, drift_control=0.5, color=RED),
    # Car(25, 10, drift_control=0.25, color=BLUE),
    Car(25, 10, max_speed=5, drift_control=0.1, color=RED, x=x, y=y, length_sensor=100)
]

environment = Environment(generator.frames, generator.rewards, generator.finish)

agent = Agent(epsilon_decay=0.99, action_size=5)

direction = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "stop": False
}

counter = 0
fps_check = 3

pre_state: np.array = None
pre_reward: np.array = 0
pre_action: np.array = 0
epoch = 0

def agent_action():
    global pre_state
    global pre_reward
    global pre_action

    direction["up"] = False
    direction["down"] = False
    direction["left"] = False
    direction["right"] = False
    direction["stop"] = False

    state = environment.get_state(cars[0])
    reward = environment.get_reward(cars[0])
    action = agent.action(state)

    if action == 0:
        direction["up"] = True
    elif action == 1:
        direction["down"] = True
    elif action == 2:
        direction["left"] = True
    elif action == 3:
        direction["right"] = True
    elif action == 4:
        direction["stop"] = True

    if pre_state is not None:
        # print(pre_reward)
        agent.update(pre_state, pre_action, pre_reward, state, 0)
        if pre_reward != 0:
            print(pre_state, pre_action, pre_reward, state, 0)
        # agent.train(64, update_epsilon=True)

    pre_state = state
    pre_reward = np.array(reward)
    pre_action = np.array(action)

def update(dt):
    global counter, environment
    global epoch
    global pre_state
    agent_action()

    for car in cars:
        if not environment.check(car):
            car.update()
        else:
            agent.update(pre_state, pre_action, np.array(-100), pre_state, 1)
            print(pre_state, pre_action, np.array(-100), pre_state, 1)
            agent.train(1024, update_epsilon=True)

            epoch += 1
            print(epoch, agent.brain.epsilon, len(agent.brain.memory))

            environment = Environment(generator.frames, generator.rewards, generator.finish)
            cars.remove(car)
            cars.append(Car(25, 10, max_speed=5, drift_control=0.1, color=RED, x=x, y=y, length_sensor=100))
            pre_state = None


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
