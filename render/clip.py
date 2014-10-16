import json
from moviepy import editor


class Clip:
    def __init__(self, jsonFilename):
        with open(jsonFilename) as f:
            self.data = json.loads(f.read())

    def duration(self):
        return self.data['endPosition'] - self.data['beginPosition']

    def description(self):
        return self.data['description']

    def width(self):
        return self.data['size'][0]

    def height(self):
        return self.data['size'][1]

    def fps(self):
        return self.data['fps']

    def filename(self):
        return self.data['filename']

    def open(self):
        orig = editor.VideoFileClip(self.filename())
        result = orig.subclip(self.data['beginPosition'], self.data['endPosition'])
        def close():
            orig.reader.close()
            orig.audio.reader.close_proc()
        result.close = close
        return result
