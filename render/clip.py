import json
from moviepy import editor
import moviepy.video.fx.all
from moviepy import video


class Clip:
    def __init__(self, data):
        self.data = data

    @classmethod
    def listFromFile(cls, jsonFilename):
        with open(jsonFilename) as f:
            data = json.loads(f.read())
        if isinstance(data, list):
            return [cls(c) for c in data]
        else:
            return [cls(data)]

    def duration(self):
        result = self.data['endPosition'] - self.data['beginPosition']
        for effect in self.data.get('effects', []):
            if effect['type'] == "modify speed":
                result /= effect['factor']
        return result

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
        for effect in self.data.get('effects', []):
            if effect['type'] == "modify speed":
                result = video.fx.all.speedx(result, factor=effect['factor'])
            else:
                raise Exception("Unknown effect: '%s'" % effect['type'])
        def close():
            orig.reader.close()
            orig.audio.reader.close_proc()
        result.close = close
        return result
