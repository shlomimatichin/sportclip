import savemodal
import subprocess
import json


class Interval:
    def __init__(self, filename, jsonsDir, clip):
        self._filename = filename
        self._jsonsDir = jsonsDir
        self._clip = clip
        self._beginPosition = None

    def setMarker(self, pos):
        if self._beginPosition is None:
            self._beginPosition = pos
        else:
            clipType = "frame" if self._beginPosition == pos else "clip"
            data = dict(
                filename=self._filename,
                fps=self._clip.fps,
                size=self._clip.size,
                duration=self._clip.duration,
                beginPosition=self._beginPosition,
                endPosition=pos,
                clipType=clipType)
            subprocess.Popen([
                "python", savemodal.__file__,
                "--jsonsDir", self._jsonsDir,
                "--json", json.dumps(data)])
            self._beginPosition = None
