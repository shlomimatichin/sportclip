from moviepy import editor
import logging
import videowriter


class Render:
    def __init__(self, clips, output, withDescription=False, fast=False):
        self._clips = clips
        self._output = output
        self._withDescription = withDescription
        self._fast = fast
        first = self._clips[0].open()
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
            logging.info("Appending clip %d" % self._clips.index(clip))
            video = clip.open()
            try:
                if self._withDescription:
                    writer.append(self._addDescriptionToVideo(video, clip))
                else:
                    writer.append(video)
            finally:
                video.close()
        writer.close()
        logging.info("Done")

    def _addDescriptionToVideo(self, video, clip):
        txt = editor.TextClip(
            clip.description(), font='Caladea', color='white',fontsize=96).on_color(
                size=(self._size[0], 128), color=(0, 0, 0), pos=(43, 'center'), col_opacity=0.6).set_pos(
                    lambda t: (0, 6 * self._size[1] / 7))
        return editor.CompositeVideoClip([video,txt]).subclip(0, video.duration)
