import time
import numpy
import threading
import pygame


class AudioPlayer(threading.Thread):
    def __init__(self, audioClip):
        self._audioClip = audioClip
        self._fps = 44100
        self._nbytes = 2
        self._bufferSize = 4000
        pygame.mixer.quit()
        pygame.mixer.init(self._fps, -8 * self._nbytes, audioClip.nchannels, 1024)
        self._lastFrame = int(self._fps * audioClip.duration)
        self._queue = []
        self._pos = None
        threading.Thread.__init__(self)
        self.daemon = True
        threading.Thread.start(self)

    def pos(self):
        return self._pos

    def play(self, fromSecond):
        pos = int(self._fps * fromSecond)
        pospos = list(range(pos, self._lastFrame, self._bufferSize))+[self._lastFrame]
        self._queue = pospos

    def run(self):
        channel = None
        while True:
            if len(self._queue) < 2:
                self._pos = None
                time.sleep(0.003)
                continue
            firstSample = self._queue[0]
            self._queue.pop(0)
            lastSample = self._queue[0]
            tt = (1.0/self._fps)*numpy.arange(firstSample, lastSample)
            sndarray = self._audioClip.to_soundarray(tt,self._nbytes)
            chunk = pygame.sndarray.make_sound(sndarray)
            if channel is None:
                channel = chunk.play()
            while channel.get_queue():
                time.sleep(0.003)
            channel.queue(chunk)
            self._pos = float(firstSample) / self._fps
