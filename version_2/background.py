import numpy
import numpy as np
from PIL import Image
import pyglet


class Background:
    image: pyglet.image
    map: numpy.array

    def __init__(self, image):
        self.image = pyglet.image.load(image)
        img = Image.open(image)
        self.map = np.array(img).clip(0, 1)

    def draw(self):
        self.image.blit(0, 0)

    def check(self, car):
        return
        # for point in car.body:
        #     x, y = point
        #     if self.map[-int(y + car.y)][int(x + car.x)] == 0:
        #         return True

    def get_map(self):
        return self.map
