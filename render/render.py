from moviepy import editor
import quickresize
import logging
import videowriter


class Render:
    def __init__(self, clips, output, withCaption=False, fast=False, downsizeFactor=None):
        self._clips = clips
        self._output = output
        self._withCaption = withCaption
        self._fast = fast
        self._downsizeFactor = downsizeFactor
        first = self._openClip(self._clips[0])
        try:
            self._size = first.size
            self._fps = first.fps
        finally:
            first.close()

    def go(self):
        writer = videowriter.VideoWriter(
            filename=self._output, size=self._size, fps=self._fps,
            preset="ultrafast" if self._fast else "medium")
        for clip in self._clips:
            logging.info("Appending clip %d/%d" % (self._clips.index(clip) + 1, len(self._clips)))
            video = self._openClip(clip)
            try:
                if self._withCaption:
                    writer.append(self._addCaptionToVideo(video, clip))
                else:
                    writer.append(video)
            finally:
                video.close()
        writer.close()
        logging.info("Done")

    def _addCaptionToVideo(self, video, clip):
        txt = editor.TextClip(
            clip.caption(), font='Caladea', color='white',fontsize=96).on_color(
                size=(self._size[0], 128), color=(0, 0, 0), pos=(43, 'center'), col_opacity=0.6).set_pos(
                    lambda t: (0, 6 * self._size[1] / 7))
        return editor.CompositeVideoClip([video,txt]).subclip(0, video.duration)

    def _openClip(self, clip):
        result = clip.open()
        if self._downsizeFactor is not None:
            quickresize.install()
            size = result.size
            result = result.resize((
                size[0] / self._downsizeFactor,
                size[1] / self._downsizeFactor))
        return result
