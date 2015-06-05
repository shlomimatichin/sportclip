import argparse
import sys
import pygame
import numpy
import time
import tempfile
import os
from pygame import locals
from moviepy import editor
from plotaudio import wrapper
import audioplayer

parser = argparse.ArgumentParser()
parser.add_argument("soundtrackClip")
args = parser.parse_args()
wave = args.soundtrackClip + ".wav"

if not os.path.exists(wave):
    wrapper.convertToWav(args.soundtrackClip, wave)
audio = editor.AudioFileClip(wave)
audioPlayer = audioplayer.AudioPlayer(audio)


class Main:
    def __init__(self, width=1000, height=200):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def MainLoop(self):
        self._createBackground(self.screen.get_size())
        self._createAudioGraph()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print "QUIT"
                    sys.exit()
                    return
                elif event.type == locals.VIDEORESIZE:
                    self._createBackground(event.size)
                    print "RESIZE", self.screen.get_size()
                    self._createAudioGraph()
                elif event.type == locals.KEYDOWN:
                    if event.key == locals.K_RIGHT:
                        print "RIGHT"
                    elif event.key == locals.K_LEFT:
                        print "LEFT"
                elif event.type == locals.MOUSEBUTTONDOWN and event.button == 1:
                    print "CLICK (%d, %d)" % event.pos
                    if self.graph.rect.collidepoint(event.pos):
                        offset = (event.pos[0] - self.graph.rect[0], event.pos[1] - self.graph.rect[1])
                        pos = audio.duration * offset[0] / self.graph.rect.width
                        print "IN", offset, pos
                        audioPlayer.play(pos)


            self.screen.blit(self.background, (0, 0))
            font = pygame.font.Font(None, 36)
            text = font.render(args.soundtrackClip, 1, (130, 130, 130))
            textpos = text.get_rect(centerx=self.background.get_width()/2)
            self.screen.blit(text, textpos)
            self.graphSprite.draw(self.screen)
            pos = audioPlayer.pos()
            if pos is not None:
                x = self.graph.rect[0] + int(pos / audio.duration * self.graph.rect.width)
                pygame.draw.line(
                    self.screen, (200, 0, 0), (x, self.graph.rect[1]),
                    (x, self.graph.rect[1] + self.graph.rect.height), 1)
            pygame.display.flip()

    def _createBackground(self, size):
        self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        self.background = pygame.Surface(size)
        self.background = self.background.convert()
        self.background.fill((40,40,40))

    def _createAudioGraph(self):
        height = 90
        width = self.screen.get_size()[0]
        imageFile = tempfile.NamedTemporaryFile(suffix=".png")
        wrapper.plot(args.soundtrackClip, width, height, imageFile.name)
        image = pygame.image.load(imageFile.name).convert()
        self.graph = pygame.sprite.Sprite()
        self.graph.image = image
        self.graph.rect = image.get_rect()
        self.graph.rect.move_ip(0, 50);
        self.graphSprite = pygame.sprite.RenderPlain(self.graph)


main = Main()
main.MainLoop()
