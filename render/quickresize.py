import moviepy.video.fx.resize
import cv2
import numpy


def _resizer(pic, newsize):
    lx, ly = int(newsize[0]), int(newsize[1])
    return cv2.resize(+pic.astype('uint8'), (lx, ly),
                      interpolation=cv2.INTER_LINEAR)
_resizer.origin = "cv2"
_installed = False


def install():
    global _installed
    if _installed:
        return
    _installed = True
    moviepy.video.fx.resize.resizer = _resizer
