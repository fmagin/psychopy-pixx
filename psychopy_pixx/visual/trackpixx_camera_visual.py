from typing import Tuple, Optional

import PIL.Image
import numpy
import numpy as np

from psychopy.visual import Window
from psychopy.visual.line import Line
from psychopy.visual.circle import Circle
from psychopy.visual.simpleimage import SimpleImageStim
from psychopy_pixx.helpers import CoordinateConverter
from pypixxlib import _libdpx as libdpx

EyePos = Tuple[float, float]
class TrackPixxCameraImage():
    #TODO: This should probably inherit from some Stimulus class, but I'm not sure which one is appropriate
    """
    This class
    """
    def __init__(self, window: Window, pos=None, units=None, markup_eyes=False):
        self.pos = pos
        self.units = units
        self.window = window
        self.markup_eyes = markup_eyes

        self.coordinate_converter = CoordinateConverter(window)

        libdpx.DPxOpen()
        if not libdpx.DPxDetectDevice("TRACKPIXX"):
            raise Exception('No TRACKPixx3 detected!')
        libdpx.DPxSetTPxAwake()
        libdpx.TPxSetLEDIntensity(7)
        libdpx.TPxClearSearchLimits()
        libdpx.DPxUpdateRegCache()

    def _to_cartesian(self, coords):
        return (coords - self.pos) * [1, -1, 1, -1]

    def _to_centered_origin(self, coords: Tuple[float, float]) -> Tuple[float, float]:
        x, y = coords
        return x - self.window.size[0] / 2, self.window.size[1] / 2 - y

    def _vpixx_to_psychopy(self, coords: Tuple[float, float]) -> Tuple[float, float]:
        assert (self.window.pos[0], self.window.pos[1]) == (0, 0), f"Window pos different than 0,0 not supported yet. Is: {self.window.pos}"
        self.window.pos
        x, y = coords
        return x, -y

    def get_pupil_coordinates(self) -> Tuple[Optional[EyePos], Optional[EyePos]]:
        """
        Returns the pupil coordinates in pixels in the coordinate space of the ImageStimuli

        this means that drawing something at this coordinate should draw it at the pupil
        :return:
        """
        # TODO: This is fairly broken currently, because correctly converting between coordinates is hard
        # The code for this should be written once as a helper (and maybe vpixx will provide this at some point?)
        # And then simply used here
        (ppLeftX, ppLeftY, ppRightX, ppRightY) = libdpx.TPxGetPupilCoordinatesInPixels()

        left_pupil = None
        right_pupil = None
        if (ppLeftX, ppLeftY) != (0, 0):
            left_pupil = np.array((ppLeftX, ppLeftY))
            (self.window.size / 2)
            x, y = self.coordinate_converter.pixels_topleft_to_center(ppLeftX, ppLeftY)

            # Making sure that we didn't screw up the types
            assert len(ppLeft) == 2, f"{ppLeft} has wrong shape, must be (2, )"

        if (ppRightX, ppRightY) != (0, 0):
            ppRight = self.pos + self.coordinate_converter.pixels_topleft_to_center(ppRightX, ppRightY)
            # Making sure that we didn't screw up the types
            assert len(ppRight) == 2, f"{ppRight} has wrong shape, must be (2, )"



        return ppLeft, ppRight



    def draw(self):
        """
        The TPXCalibrationTesting.py Script calls DPxUpdateRegCache before getting the new image,
        but this doesn't seem to be needed in practice, calling this .draw method in a loop still results
        in an updated camera image every frame

        BUT getting the current pupil coordinates does require calling DPxUpdateRegCache
        :return:
        """
        # Get the image as a numpy array
        pil_image = PIL.Image.fromarray(libdpx.TPxGetEyeImage())
        # Create a SimpleImageStim
        image_stim = SimpleImageStim(self.window, image=pil_image, pos=self.pos, units=self.units)
        image_stim.draw()
        if self.markup_eyes:
            libdpx.DPxUpdateRegCache()
            # This code is fairly directly adapted from TPxCalibrationTesting
            expected_iris_size = libdpx.TPxGetIrisExpectedSize()

            # (ppLeftMajor, _, ppRightMajor, _) = libdpx.TPxGetPupilSize() # Convert to Cartesian
            # Coordinates in Screenspace with origin in the Top Left of the camera window(I think?)


            ppLeft, ppRight = self.get_pupil_coordinates()



            # TODO: Coordinate System conversions shenanigans
            #
            # (ppLeftX, ppLeftY, ppRightX, ppRightY) = libdpx.TPxGetCRCoordinatesInPixels()
            # print(ppLeftX, ppLeftY)


            if ppLeft:
                Circle(self.window,
                       lineColor='blue',

                       units='pix',
                       pos=ppLeft,
                       radius=expected_iris_size,
                       lineWidth=2
                       ).draw()
            if ppRight:
                Circle(self.window,
                       lineColor='red',
                       units='pix',
                       pos=ppRight,
                       radius=expected_iris_size,
                       lineWidth=2
                       ).draw()

            # # Create right eye markup in red
            # Line(self.window, lineColor=(1, -1, -1), units='pix',
            #             start=(camRight[0], camRight[1] - ppRightMajor / 2),
            #             end=(camRight[0], camRight[1] + ppRightMajor / 2), lineWidth=2).draw()
            # Line(self.window, lineColor=(1, -1, -1), units='pix',
            #             start=(camRight[0] - ppRightMajor / 2, camRight[1]),
            #             end=(camRight[0] + ppRightMajor / 2, camRight[1]), lineWidth=2).draw()
            # Circle(self.window, lineColor=(1, -1, -1), units='pix', pos=camRight, radius=expectedIrisSize / 2,
            #               lineWidth=2).draw()

            #
            pass
