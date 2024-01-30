import pyglet

from ai.agent import Agent
from function.function import RED
from game.car import Car
from game.game_controller import GameController

screen = pyglet.canvas.get_display().get_default_screen()
screen_width, screen_height = screen.width, screen.height

height = 768
width = 1024

x = (screen_width - width) // 2
y = (screen_height - height) // 2

agent = Agent(epsilon_decay=0.995, action_size=5, epsilon_min=0.02)
window = pyglet.window.Window(width=width, height=height, caption='Races AI')
window.set_location(x, y)

car = Car(25, 10, max_speed=5, drift_control=0.1, color=RED, length_sensor=150)
game_controller = GameController(car=car, agent=agent, reward_move=0.0, frequency_ai=2)


def update(dt):
    game_controller.update()


@window.event
def on_draw():
    window.clear()
    game_controller.draw()


@window.event
def on_key_press(symbol, modifiers):
    game_controller.on_key_press(symbol, modifiers)


@window.event
def on_key_release(symbol, modifiers):
    game_controller.on_key_release(symbol, modifiers)



pyglet.clock.schedule_interval(update, 1.0 / game_controller.fps)
pyglet.app.run()
