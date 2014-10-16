# based on moviepy.video.VideoClip.write_videofile and moviepy.video.io.ffmpeg_writer.ffmpeg_write_video
import os
from moviepy import tools
from moviepy.video.io import ffmpeg_writer


class VideoWriter:
    def __init__(self,
                 filename,
                 size=(1920, 1080),
                 fps=29.97,
                 codec=None,
                 bitrate=None,
                 preset="medium",
                 writeLogfile=False):
        self._size = size
        self._fps = fps

        name, ext = os.path.splitext(os.path.basename(filename))
        ext = ext[1:].lower()

        if codec is None:
            codec = self._guessCodec(filename)

        self._logfile = None
        if writeLogfile:
            self._logfile = open(filename + ".log", 'w+')

        self._writer = ffmpeg_writer.FFMPEG_VideoWriter(
            filename, size, fps, codec=codec, preset=preset,
            bitrate=None, logfile=self._logfile, audiofile=None)

    def append(self, clip):
        for t, frame in clip.iter_frames(progress_bar=True, with_times=True, fps=self._fps):
            self._writer.write_frame(frame.astype("uint8"))

    def _guessCodec(self, filename):
        name, ext = os.path.splitext(os.path.basename(filename))
        ext = ext[1:].lower()
        try:
            return tools.extensions_dict[ext]['codec'][0]
        except KeyError:
            raise ValueError(
               "MoviePy couldn't find the codec associated "
               "with the filename. Provide the 'codec' parameter in "
               "write_fideofile.")

    def close(self):
        self._writer.close()
        if self._logfile is not None:
            self._logfile.close()
