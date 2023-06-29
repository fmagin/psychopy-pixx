from pyglet.canvas import Display
#
display = Display(x_screen=1)


from psychopy import event
from psychopy.visual import Window
from psychopy_pixx.visual.trackpixx_camera_visual import TrackPixxCameraImage

window = Window(fullscr=True,
                # color=-1,
                screen=1,  # TODO: For now this is hardcoded,
                size=(1920, 1080),
                )

camera = TrackPixxCameraImage(window, pos=(-320, 284), units='pix', markup_eyes=False)


while not event.getKeys(keyList=["escape"]):
    camera.draw()
    window.flip()
