import numpy
import numpy as np
from PIL import Image
import pyglet


class Background:
    image: pyglet.image

    def __init__(self, image):
        self.image = pyglet.image.load(image)

    def draw(self):
        # pass
        self.image.blit(0, 0)
