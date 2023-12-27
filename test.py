import pyglet

# Размеры прямоугольника
rectangle_width = 200
rectangle_height = 100

# Создание окна Pyglet
window = pyglet.window.Window(width=800, height=600)

# Создание прямоугольника с использованием pyglet.graphics.vertex_list
rectangle = pyglet.graphics.vertex_list(4,
                                       ('v2f', [-rectangle_width / 2, -rectangle_height / 2,
                                                 rectangle_width / 2, -rectangle_height / 2,
                                                 rectangle_width / 2, rectangle_height / 2,
                                                 -rectangle_width / 2, rectangle_height / 2]),
                                       ('c3B', (255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 255)))

@window.event
def on_draw():
    window.clear()
    rectangle.draw(pyglet.gl.GL_QUADS)

pyglet.app.run()
