from psychopy.monitors import Monitor
from psychopy.visual import Window
from psychopy_pixx.helpers import CoordinateConverter


def test_coord_transform():

    # Fullscreen window
    monitor = Window(size=(1920, 1080), pos=(0, 0), units='pix', fullscr=True, screen=1)

    converter = CoordinateConverter(monitor)

    # the origin of the Monitorspace
    assert converter.pixels_topleft_to_center(0, 0) == (-(1920 / 2), (1080/2))

    #
