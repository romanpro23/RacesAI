RED = (255, 0, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)


def sign(numb):
    return 0 if numb == 0 else abs(numb) / numb


def clip(numb, numb_min, numb_max):
    return min(max(numb, numb_min), numb_max)
