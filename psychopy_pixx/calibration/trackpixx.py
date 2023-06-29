from typing import Sequence, Tuple, Optional, List, Callable

import PIL.Image

# # from psychopy.visual.shape import BaseShapeStim
# from pyglet.canvas import Display
#
# display = Display(x_screen=1)

from psychopy.visual.circle import Circle
from psychopy.visual.simpleimage import SimpleImageStim
from psychopy.visual.window import Window
from psychopy.visual.text import TextStim
from psychopy.visual.line import Line
from pypixxlib.tracker import Tracker
from pypixxlib import _libdpx as libdpx
from psychopy import event

ScreenPercentage = float
# Type alias for a float that represents a coordinate as an absolute value
# It doesn't imply a coordinate system, i.e. it could be relative to the center, or the top left corner
ScreenAbsolute = float

Point = Tuple[
    ScreenPercentage, ScreenPercentage
]  # TODO: type for coordinate system, cartesian vs polar


def _default_points(
    window_dimensions: Tuple[int, int],
    pscr: float = 0.7,  # TODO: What actually is that, needs a better name
) -> List[Point]:
    """
    The idea is that this method returns the default list of points to calibrate on.
    This is a function because the position depends on the size of the window, if they should be in pixel coordinates
    In theory they could also be just returned as normed coordinates (i.e. between 0 and 1), I can't
    :param window_dimensions: just pass `window.size` of the PsychoPy window
    :param pscr: unclear
    :return:
    """
    print(window_dimensions)
    scrw, scrh = window_dimensions
    # points = [(0, 0), (0, scrh / 2 * pscr), (scrw / 2 * pscr, 0), (0, -scrh / 2 * pscr), (-scrw / 2 * pscr, 0),
    #           (scrw / 2 * pscr, scrh / 2 * pscr), (scrw / 2 * pscr, -scrh / 2 * pscr),
    #           (-scrw / 2 * pscr, scrh / 2 * pscr),
    #           (-scrw / 2 * pscr, -scrh / 2 * pscr)]
    points = [
        (0, 0),
        (0.5, 0.5),
        (1, 1),
    ]

    return points

def run_calibration(
    window: Window,
    tracker: Tracker,  # Unclear what types we can support here, might be TRACKPixx3 specific
    points: Optional[Sequence[Point]] = None,
    # stimulus: Callable[[Window, Point], BaseShapeStim] = lambda w, p: Circle(w, pos=p, radius=0.01)
) -> None:
    """

    :param window: the PsychoPy window to user
    :param tracker: The Tracker object to use
    :param points: A custom Sequence (e.g. a list or a np.array) of points to calibrate on
    :param stimulus: A function that takes a window and a point and returns a stimulus to draw
    :return: TODO: tracker.isDeviceCalibrated might be sensible, but maybe an exception for failed calib is better?
    """
    print("Calibration Requested")
    tracker.clearDeviceCalibration()
    starting_text = TextStim(
        window,
        units="norm",
        text=(
            "Manual calibration: For each point, press any key when ready for calibration. Press any key to start"
        ),
        wrapWidth=0.9,
    )
    starting_text.draw()
    window.flip()
    event.waitKeys()
    print("Starting Calibration")
    points = points or _default_points(window.size)

    for point in points:
        assert (1, 1) >= point >= (-1, -1), "Point must be in range [-1, 1]"

    for point in points:
        p = Circle(window, pos=point, radius=0.01)
        print(point)
        p.draw()
        window.flip()
        event.waitKeys()
        # calibrates the first eye for point p
        # tracker.getEyePositionDuringCalib(p.pos[0], p.pos[1], 0)
        # calibrates the second eye for point p
        # tracker.getEyePositionDuringCalib(p.pos[0], p.pos[1], 1)

    starting_text = TextStim(
        window,
        units="norm",
        text=("Finished Calibration. Press any key to return."),
        wrapWidth=0.9,
    )
    starting_text.draw()
    window.flip()
    event.waitKeys()

def is_valid_eye_pos(eye_pos: Tuple[ScreenAbsolute, ScreenAbsolute, ScreenAbsolute, ScreenAbsolute]) -> bool:
    """
    For unclear reasons the eye position can be 32767.0, which is not a valid position
    This is probably some kind of bug in the tracker:
    32767 is the maximum value for a signed 16-bit integer, and at some point this seems to get converted to a float

    I also can't think of why this would be a good error value, but maybe this is intentional.
    If it's float, using NaN would seem like the more appropriate option
    :param eye_pos: 
    :return: 
    """
    for coord in eye_pos:
        if coord == 32767.0:
            return False
    return True


def show_eyepos(
    window: Window,
    tracker: Tracker,
):
    """
    This method should be a simple demo that just grabs the current eye position and renders a small circle in psychopy
    at that position.
    Can be used for manually testing the calibration results, and as a general eye tracking demo
    :param window:
    :param tracker:
    :return:
    """
    assert tracker.isDeviceCalibrated(), "Tracker is not calibrated"
    # TODO: unclear if this works in the current state
    while True:
        if event.getKeys(keyList=["escape"]):
            break
        eye_pos: Tuple[ScreenAbsolute, ScreenAbsolute, ScreenAbsolute, ScreenAbsolute] = tracker.getEyePosition()

        if not is_valid_eye_pos(eye_pos):
            continue

        x, y = eye_pos[0] / window.size[0] * 2, eye_pos[1] / window.size[1] * 2
        print(x, y)
        eye_pos_rel = tracker.convertCoordSysToCartesian([eye_pos])
        # text = TextStim(
        #     window,
        #     units="norm",
        #     text=f"({x}, {y})",
        #     wrapWidth=0.9,
        # )
        # text.draw()

        print(list(eye_pos))
        print(eye_pos_rel)
        # assert (1, 1) >= (x, y) >= (-1, -1), f"Point must be in range [-1, 1], was {x}, {y}"
        p = Circle(window, pos=(x, y), radius=0.01)
        p.draw()
        window.flip()




def run_validation(
    window: Window,
    tracker: Tracker,
    points: Sequence[Point] = None,
):
    # TODO
    pass


if __name__ == "__main__":
    from psychopy.visual import Window
    from pypixxlib.tracker import TRACKPixx3

    w = Window(
        fullscr=True,
        size=(1920, 1080),
        # x_screen=1,
        screen=1,
        color=[-1, -1, -1],
        winType="pyglet",
    )

    tracker = TRACKPixx3()
    tracker.open()
    tracker.setLEDintensity(7)
    tracker.setIrisSize(50, 67)
    tracker.showOverlay()

    print("Finished Tracker Setup")
    run_calibration(window=w, tracker=tracker)

    w.flip()
    tracker.hideOverlay()

    w.close()
